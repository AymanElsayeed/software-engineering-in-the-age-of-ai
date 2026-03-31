"""
This file is the main entry point for the support pipeline.
It orchestrates the agent_a and agent_b, and the semantic cache.
It also handles the cache threshold and hitl auto approve.
It also handles the question and the result.

"""

from __future__ import annotations


import sys
import os
from pathlib import Path
from typing import Any


_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Keep Agent A/B on in-memory vdb for local demo stability.
# Cache persistence is handled via utils.tvdb (Weaviate cloud) below.
os.environ.setdefault("USE_WEAVIATE", "0")

from agent_a import agent_a
from agent_b import agent_b
from utils.orchestrator import SupportPipelineOrchestrator
from utils.tvdb import add_cache_entry, semantic_cache_lookup



_pipeline_orchestrator = SupportPipelineOrchestrator(
    agent_a_fn=agent_a,
    agent_b_fn=agent_b,
    semantic_cache_lookup_fn=semantic_cache_lookup,
    add_cache_entry_fn=add_cache_entry,
)

cache_threshold: float = 0.86
hitl_auto_approve: bool = True
question: str = "How to reset my password on my account"
result = _pipeline_orchestrator.run_pipeline(
        question,
        cache_threshold=cache_threshold,
        hitl_auto_approve=hitl_auto_approve,
    )
print(result)
