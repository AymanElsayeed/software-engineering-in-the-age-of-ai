"""
GPT / OpenAI helpers with an orchestrator-style dual-provider fallback.

Agent A: gpt-4o-mini (cheaper). 

Agent B: gpt-4o (or gpt-4o-mini if 4o unavailable).

"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Sequence
from dotenv import load_dotenv
from openai import OpenAI
from utils.logging_config import get_task2_logger
from utils.orchestrator import LLMOrchestrator

logger = get_task2_logger(__name__)


Message = dict[str, str]


def _client() -> Any:
    load_dotenv()  # reads .env from current folder
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=key)


def _extract_text(response: Any) -> str:
    choice = response.choices[0]
    content = choice.message.content
    if content is None:
        return ""
    return content.strip()


@dataclass
class ChatCompletionResult:
    text: str
    model_used: str
    provider_label: str


class OpenAIChatProvider:
    """Single-model OpenAI chat completion."""

    _MODEL_PRICES_PER_1M: dict[str, tuple[float, float]] = {
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4o": (5.00, 15.00),
    }

    def __init__(
        self,
        model: str,
        label: str,
        fallback_model: str | None = None,
        attempt_budget: int | None = None,
        timeout_budget: float | None = None,
        cost_budget_usd: float | None = None,
    ) -> None:
        self.model = model
        self.label = label
        env_label = label.upper()
        self.fallback_model = fallback_model or os.environ.get(f"OPENAI_{env_label}_FALLBACK_MODEL", "gpt-4o")
        self.attempt_budget = attempt_budget if attempt_budget is not None else int(
            os.environ.get(f"OPENAI_{env_label}_ATTEMPT_BUDGET", "2")
        )
        self.timeout_budget = timeout_budget if timeout_budget is not None else float(
            os.environ.get(f"OPENAI_{env_label}_TIMEOUT_BUDGET", "120")
        )
        self.cost_budget_usd = cost_budget_usd if cost_budget_usd is not None else float(
            os.environ.get(f"OPENAI_{env_label}_COST_BUDGET_USD", "1.00")
        )

    def _estimate_cost_usd(self, response: Any, model_name: str) -> float:
        usage = getattr(response, "usage", None)
        if usage is None:
            return 0.0
        prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        prompt_price, completion_price = self._MODEL_PRICES_PER_1M.get(model_name, (0.0, 0.0))
        return (prompt_tokens / 1_000_000 * prompt_price) + (completion_tokens / 1_000_000 * completion_price)

    def complete(self, messages: Sequence[Message], timeout: float = 60.0) -> ChatCompletionResult:
        logger.info(f"Calling GPT with model: {self.model}")
        client = _client()
        elapsed_timeout = 0.0
        total_cost_usd = 0.0
        attempts = 0
        models_to_try = [self.model]
        if self.fallback_model and self.fallback_model != self.model:
            models_to_try.append(self.fallback_model)

        last_error: Exception | None = None
        for model_name in models_to_try:
            if attempts >= self.attempt_budget:
                break
            if elapsed_timeout >= self.timeout_budget:
                break
            if total_cost_usd >= self.cost_budget_usd:
                break

            call_timeout = min(timeout, max(0.0, self.timeout_budget - elapsed_timeout))
            if call_timeout <= 0:
                break

            attempts += 1
            started_at = time.monotonic()
            try:
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=list(messages),
                    timeout=call_timeout,
                )
                logger.info(f"GPT response: {resp}")
                elapsed_timeout += time.monotonic() - started_at
                total_cost_usd += self._estimate_cost_usd(resp, model_name)
                if total_cost_usd > self.cost_budget_usd:
                    raise RuntimeError(
                        f"{self.label} exceeded cost budget (${self.cost_budget_usd:.4f}) during completion."
                    )
                return ChatCompletionResult(
                    text=_extract_text(resp),
                    model_used=model_name,
                    provider_label=self.label,
                )
            except Exception as e:
                elapsed_timeout += time.monotonic() - started_at
                last_error = e
                logger.warning(
                    "Provider %s failed on model=%s (attempt=%d/%d): %s",
                    self.label,
                    model_name,
                    attempts,
                    self.attempt_budget,
                    e,
                )

        raise RuntimeError(
            f"{self.label} exhausted fallback strategy (attempt_budget={self.attempt_budget}, "
            f"timeout_budget={self.timeout_budget:.2f}s, cost_budget_usd={self.cost_budget_usd:.4f}). "
            f"Last error: {last_error}"
        )


_default_orchestrator: LLMOrchestrator | None = None


def get_default_adapter() -> LLMOrchestrator:
    global _default_orchestrator
    if _default_orchestrator is None:
        agent_a_model = os.environ.get("OPENAI_MODEL_PRIMARY", "gpt-4o-mini")
        agent_b_model = os.environ.get("OPENAI_MODEL_FALLBACK", "gpt-4o")
        _default_orchestrator = LLMOrchestrator(
            agent_a=OpenAIChatProvider(agent_a_model, "agent_a"),
            agent_b=OpenAIChatProvider(agent_b_model, "agent_b"),
        )
    return _default_orchestrator


def call_gpt_with_system_prompt_and_user_prompt(
    system_prompt: str,
    user_prompt: str,
    *,
    model: str | None = None,
    timeout: float = 60.0,
    provider_label: str = "direct",
    fallback_model: str | None = None,
    attempt_budget: int | None = None,
    timeout_budget: float | None = None,
    cost_budget_usd: float | None = None,
) -> ChatCompletionResult:
    """
    If ``model`` is set, uses that model only (no fallback). Otherwise uses the default adapter.
    """
    messages: list[Message] = [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt},]
    if model:
        logger.info(f"Calling GPT with model: {model}")
        return OpenAIChatProvider(
            model,
            provider_label,
            fallback_model=fallback_model,
            attempt_budget=attempt_budget,
            timeout_budget=timeout_budget,
            cost_budget_usd=cost_budget_usd,
        ).complete(messages, timeout=timeout)
    return get_default_adapter().complete(messages, timeout=timeout)


def call_gpt_with_context(system_prompt: str, user_prompt: str, context: str, *, model: str | None = None, timeout: float = 60.0,) -> ChatCompletionResult:
    merged_user = f"Context:\n{context}\n\nUser question:\n{user_prompt}"
    logger.info(f"Calling GPT with context: {merged_user}")
    return call_gpt_with_system_prompt_and_user_prompt(
        system_prompt,
        merged_user,
        model=model,
        timeout=timeout,
    )
