"""
Agent B: propose a support answer from Agent A output + optional semantic cache hints.

Uses utils.gpt (adapter) and utils.vdb.get_similar_questions for cache-style hints.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

from agent_a import AgentAResult
from utils.gpt import call_gpt_with_system_prompt_and_user_prompt
from utils.logging_config import get_task2_logger
from utils.vdb import get_similar_questions

logger = get_task2_logger(__name__)


@dataclass
class AgentBResult:
    answer: str
    confidence: float
    model_used: str
    provider_label: str


def _parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        text = m.group(0)
    return json.loads(text)


class AgentB:
    def __init__(self) -> None:
        self.model = os.environ.get("OPENAI_AGENT_B_MODEL", "gpt-4o")
        self.fallback_model = os.environ.get("OPENAI_AGENT_B_FALLBACK_MODEL", "gpt-4o-mini")
        self.attempt_budget = int(os.environ.get("OPENAI_AGENT_B_ATTEMPT_BUDGET", "2"))
        self.timeout_budget = float(os.environ.get("OPENAI_AGENT_B_TIMEOUT_BUDGET", "120"))
        self.cost_budget_usd = float(os.environ.get("OPENAI_AGENT_B_COST_BUDGET_USD", "1.00"))

    def run(self, question: str, agent_a_result: AgentAResult, model: str | None = None) -> AgentBResult:
        """
        Generate a user-facing answer. ``model`` overrides this agent model.
        """
        logger.debug("agent_b start category=%s", agent_a_result.category)
        hints = get_similar_questions(question, top_k=3)
        hint_lines = []
        for h in hints:
            if h.get("answer"):
                hint_lines.append(f"- Similar Q: {h['text'][:200]}… → cached A: {h['answer'][:300]}…")

        system = """You are Agent B for customer support.
                    Respond with a single JSON object only, no markdown, keys:
                    - answer (string): clear steps for the user
                    - confidence (number 0.0-1.0): your confidence the answer is correct given the context
                    - needs_human (boolean): true if policy, billing dispute, or missing info requires a human
                    """

        user = f"""Original user message:
                   {question}
                   Agent A analysis:
                   - category: {agent_a_result.category}
                   - severity: {agent_a_result.severity}
                   - rewritten_query: {agent_a_result.rewritten_query}
                   - summary: {agent_a_result.analysis_summary}
                   Knowledge base context:
                   {agent_a_result.retrieved_context or "(none)"}
                   Optional semantic-cache hints:
                   {chr(10).join(hint_lines) if hint_lines else "(none)"}
                   """

        raw = call_gpt_with_system_prompt_and_user_prompt(
            system,
            user,
            model=model or self.model,
            provider_label="agent_b",
            fallback_model=self.fallback_model,
            attempt_budget=self.attempt_budget,
            timeout_budget=self.timeout_budget,
            cost_budget_usd=self.cost_budget_usd,
        )
        try:
            data = _parse_json_object(raw.text)
        except (json.JSONDecodeError, ValueError):
            return AgentBResult(
                answer=raw.text,
                confidence=0.5,
                model_used=raw.model_used,
                provider_label=raw.provider_label,
            )

        conf = float(data.get("confidence", 0.7))
        conf = max(0.0, min(1.0, conf))
        answer = str(data.get("answer", raw.text))
        if data.get("needs_human"):
            conf = min(conf, 0.6)

        return AgentBResult(
            answer=answer,
            confidence=conf,
            model_used=raw.model_used,
            provider_label=raw.provider_label,
        )


_agent_b = AgentB()


def agent_b(question: str, agent_a_result: AgentAResult, model: str | None = None) -> AgentBResult:
    return _agent_b.run(question, agent_a_result, model=model)
