from __future__ import annotations

from typing import Any, Callable, Protocol, Sequence

from utils.logging_config import get_task2_logger


logger = get_task2_logger(__name__)

Message = dict[str, str]


class ChatCompletionResultLike(Protocol):
    text: str
    model_used: str
    provider_label: str


class ChatProvider(Protocol):
    label: str

    def complete(self, messages: Sequence[Message], timeout: float = 60.0) -> ChatCompletionResultLike:
        ...


class LLMOrchestrator:
    """
    Orchestrator: one interface, two concrete providers.
    On Agent A failure, falls back to Agent B.
    """

    def __init__(
        self,
        agent_a: ChatProvider,
        agent_b: ChatProvider,
        on_fallback: Callable[[Exception], None] | None = None,
    ) -> None:
        self._agent_a = agent_a
        self._agent_b = agent_b
        self._on_fallback = on_fallback

    def complete(self, messages: Sequence[Message], timeout: float = 60.0) -> ChatCompletionResultLike:
        try:
            return self._agent_a.complete(messages, timeout=timeout)
        except Exception as e:  # noqa: BLE001 - intentional broad catch for fallback
            logger.warning("Agent A failed (%s), falling back to Agent B: %s", self._agent_a.label, e)
            if self._on_fallback:
                self._on_fallback(e)
            return self._agent_b.complete(messages, timeout=timeout)


class SupportPipelineOrchestrator:
    """
    End-to-end support pipeline:
    semantic cache -> Agent A (guard + analysis) -> Agent B -> HITL -> cache write.
    """

    _SENSITIVE_CATEGORIES = frozenset({"billing", "security", "legal", "account"})

    def __init__(
        self,
        agent_a_fn: Callable[[str], Any],
        agent_b_fn: Callable[[str, Any], Any],
        semantic_cache_lookup_fn: Callable[[str, float], str | None],
        add_cache_entry_fn: Callable[[str, str], Any],
    ) -> None:
        self._agent_a_fn = agent_a_fn
        self._agent_b_fn = agent_b_fn
        self._semantic_cache_lookup_fn = semantic_cache_lookup_fn
        self._add_cache_entry_fn = add_cache_entry_fn

    def _needs_hitl(self, confidence: float, category: str, severity: str, fallback_used: bool) -> bool:
        if confidence < 0.75:
            return True
        if category.lower() in self._SENSITIVE_CATEGORIES:
            return True
        if severity.lower() == "high":
            return True
        if fallback_used:
            return True
        return False

    def run_pipeline(self, question: str, *, cache_threshold: float = 0.86, hitl_auto_approve: bool = True) -> dict[str, Any]:
        logger.info(f"Running pipeline for question: {question}")
        cached = self._semantic_cache_lookup_fn(question, threshold=cache_threshold)
        if cached:
            logger.info("semantic_cache hit (preview answer=%r)", (cached[:200] + "...") if len(cached) > 200 else cached)
            return {
                "answer": cached,
                "source": "semantic_cache",
                "hitl_required": False,
                "hitl_approved": True,
                "agent_a": None,
                "agent_b": None,
            }

        a_out = self._agent_a_fn(question)
        logger.info(f"agent_a output: {a_out}", )
        if a_out.guard_blocked:
            return {
                "answer": a_out.guard_reason,
                "source": "guard",
                "hitl_required": True,
                "hitl_approved": False,
                "agent_a": {
                    "category": a_out.category,
                    "severity": a_out.severity,
                    "guard_blocked": True,
                },
                "agent_b": None,
            }

        b_out = self._agent_b_fn(question, a_out)
        fallback_used = b_out.provider_label == "agent_b"
        hitl = self._needs_hitl(b_out.confidence, a_out.category, a_out.severity, fallback_used)

        if hitl and not hitl_auto_approve:
            return {
                "answer": "",
                "source": "hitl_pending",
                "hitl_required": True,
                "hitl_approved": False,
                "draft_answer": b_out.answer,
                "agent_a": {
                    "category": a_out.category,
                    "severity": a_out.severity,
                    "analysis_summary": a_out.analysis_summary,
                },
                "agent_b": {
                    "confidence": b_out.confidence,
                    "model_used": b_out.model_used,
                    "provider_label": b_out.provider_label,
                },
            }

        final = b_out.answer
        self._add_cache_entry_fn(question, final, meta={"confidence": b_out.confidence})
        return {
            "answer": final,
            "source": "mas_llm",
            "hitl_required": hitl,
            "hitl_approved": hitl_auto_approve or not hitl,
            "agent_a": {
                "category": a_out.category,
                "severity": a_out.severity,
                "analysis_summary": a_out.analysis_summary,
            },
            "agent_b": {
                "confidence": b_out.confidence,
                "model_used": b_out.model_used,
                "provider_label": b_out.provider_label,
            },
        }