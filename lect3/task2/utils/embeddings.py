"""OpenAI text embeddings (shared by in-memory vdb and Weaviate)."""

from __future__ import annotations

import os
from dotenv import load_dotenv
from openai import OpenAI
from logging_config import get_task2_logger

logger = get_task2_logger(__name__)

_EMBED_MODEL = "text-embedding-3-small"



def embed_text(text: str) -> list[float]:
    """
    Requires ``OPENAI_API_KEY``. Used for Weaviate ``self_provided`` vectors.
    """
    load_dotenv()  # reads .env from current folder
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for embeddings (Weaviate vector inserts/search).")
    client = OpenAI(api_key=key)
    r = client.embeddings.create(model=_EMBED_MODEL, input=text[:8000])
    logger.info(f"Embedding text: {text} with model: {_EMBED_MODEL}")
    return list(r.data[0].embedding)


def embed_text_optional(text: str) -> list[float] | None:
    """Same as ``embed_text`` when key is set; otherwise ``None`` (in-memory difflib fallback)."""
    if OpenAI is None or not os.environ.get("OPENAI_API_KEY"):
        return None
    try:
        return embed_text(text)
    except Exception:
        return None
