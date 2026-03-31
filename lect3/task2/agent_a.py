"""
Agent A: guardrails + issue analysis + RAG context retrieval.

Uses utils.gpt (adapter with primary/fallback) and utils.vdb for KB search.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

from utils.gpt import call_gpt_with_system_prompt_and_user_prompt
from utils.logging_config import get_task2_logger
from utils.vdb import get_context

logger = get_task2_logger(__name__)

_MAX_LEN = 8000
_SENSITIVE_HINTS = ("suicide", "self-harm", "kill myself")


@dataclass
class AgentAResult:
    category: str
    severity: str
    rewritten_query: str
    analysis_summary: str
    retrieved_context: str
    guard_blocked: bool
    guard_reason: str
    raw_llm: dict[str, Any] | None = None


def _guard_local(question: str) -> tuple[bool, str]:
    q = question.strip()
    if not q:
        return True, "Empty question."
    if len(q) > _MAX_LEN:
        return True, "Question exceeds maximum length."
    low = q.lower()
    for hint in _SENSITIVE_HINTS:
        if hint in low:
            return True, "Escalate to human crisis or safety resources; automated support cannot handle this."
    logger.debug("guard_local passed (len=%d)", len(q))
    return False, ""


def _parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        text = m.group(0)
    return json.loads(text)


class AgentA:
    def __init__(self) -> None:
        self.model = os.environ.get("OPENAI_AGENT_A_MODEL", "gpt-4o-mini")
        self.fallback_model = os.environ.get("OPENAI_AGENT_A_FALLBACK_MODEL", "gpt-4o")
        self.attempt_budget = int(os.environ.get("OPENAI_AGENT_A_ATTEMPT_BUDGET", "2"))
        self.timeout_budget = float(os.environ.get("OPENAI_AGENT_A_TIMEOUT_BUDGET", "120"))
        self.cost_budget_usd = float(os.environ.get("OPENAI_AGENT_A_COST_BUDGET_USD", "1.00"))

    def run(self, question: str, model: str | None = None) -> AgentAResult:
        logger.debug("agent_a start (len=%d)", len(question))
        blocked, reason = _guard_local(question)
        if blocked:
            return AgentAResult(
                category="blocked",
                severity="high",
                rewritten_query=question,
                analysis_summary="",
                retrieved_context="",
                guard_blocked=True,
                guard_reason=reason,
            )

        retrieved = get_context(question, top_k=3)

        system = """You are Agent A for customer support triage.
                    You must respond with a single JSON object only, no markdown, keys:
                    - category (string, e.g. billing, technical, account, security, general)
                    - severity (one of: low, medium, high)
                    - rewritten_query (string, concise search-friendly version of the issue)
                    - analysis_summary (string, 2-4 sentences)
                    - safe_to_automate (boolean): false if legal, threats, self-harm, harassment, or account takeover suspected
                    """

        user = f"""User message: {question} Retrieved knowledge snippets (may be incomplete): {retrieved or "(none)"} """

        raw = call_gpt_with_system_prompt_and_user_prompt(
            system,
            user,
            model=model or self.model,
            provider_label="agent_a",
            fallback_model=self.fallback_model,
            attempt_budget=self.attempt_budget,
            timeout_budget=self.timeout_budget,
            cost_budget_usd=self.cost_budget_usd,
        )

        try:
            data = _parse_json_object(raw.text)
        except (json.JSONDecodeError, ValueError):
            data = {
                "category": "general",
                "severity": "medium",
                "rewritten_query": question,
                "analysis_summary": raw.text[:500],
                "safe_to_automate": True,
            }
            logger.error(f"Error parsing JSON object: {raw.text}")

        if not data.get("safe_to_automate", True):
            return AgentAResult(
                category=str(data.get("category", "general")),
                severity="high",
                rewritten_query=str(data.get("rewritten_query", question)),
                analysis_summary=str(data.get("analysis_summary", "")),
                retrieved_context=retrieved,
                guard_blocked=True,
                guard_reason="Model flagged issue for human review (safety/policy).",
                raw_llm=data,
            )

        return AgentAResult(
            category=str(data.get("category", "general")),
            severity=str(data.get("severity", "medium")),
            rewritten_query=str(data.get("rewritten_query", question)),
            analysis_summary=str(data.get("analysis_summary", "")),
            retrieved_context=retrieved,
            guard_blocked=False,
            guard_reason="",
            raw_llm=data,
        )


_agent_a = AgentA()


def agent_a(question: str, model: str | None = None) -> AgentAResult:
    return _agent_a.run(question, model=model)

if __name__ == "__main__":
    result = agent_a(question="How to reset my password on my account")
    print(result)