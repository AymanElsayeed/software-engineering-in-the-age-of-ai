"""
Shared logging for all Task 2 code under the ``task2`` logger hierarchy.

Every module should use::

    from utils.logging_config import get_task2_logger
    logger = get_task2_logger(__name__)

Log records propagate to the ``task2`` root logger, which writes to stderr and (by default) to
``lect3/task2/logs/<YYYY-mm-dd_HH-MM-SS>.log``. Each line includes logger name, module (file stem),
function, and line number of the call site.

Environment (``TASK2_*`` preferred; ``WEAVIATE_*`` log paths kept for backward compatibility):

- ``TASK2_LOG_LEVEL``: ``DEBUG``, ``INFO`` (default), ``WARNING``, …
- ``TASK2_LOG_TO_FILE``: set to ``0`` / ``false`` to disable the file handler
- ``TASK2_LOG_FILE``: full path to a single log file (parent dirs created)
- ``TASK2_LOG_DIR``: directory for auto-named ``<date-time>.log`` files (default: ``task2/logs``)
- If ``TASK2_LOG_*`` unset, ``WEAVIATE_LOG_FILE`` / ``WEAVIATE_LOG_DIR`` are used for the file target
- ``TASK2_LOG_CONSOLE``: set to ``0`` / ``false`` to disable stderr logging
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_LOGGER_NAME = "task2"

_configured = False
# %(module)s = filename without .py; %(funcName)s / %(lineno)d = call site
_LOG_FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] %(module)s.%(funcName)s:%(lineno)d — %(message)s"
)


def _env_truthy(name: str, default: bool = True) -> bool:
    v = os.environ.get(name)
    if v is None or v.strip() == "":
        return default
    return v.strip().lower() not in ("0", "false", "no", "off")


def configure_task2_logging() -> None:
    """Attach handlers to the ``task2`` root logger once per process."""
    global _configured
    if _configured:
        return

    base = logging.getLogger(ROOT_LOGGER_NAME)
    base.setLevel(logging.DEBUG)
    base.propagate = False

    fmt = logging.Formatter(_LOG_FORMAT)
    level_name = (os.environ.get("TASK2_LOG_LEVEL") or "INFO").strip().upper()
    console_level = getattr(logging, level_name, logging.INFO)

    if _env_truthy("TASK2_LOG_CONSOLE", default=True):
        sh = logging.StreamHandler(sys.stderr)
        sh.setLevel(console_level)
        sh.setFormatter(fmt)
        base.addHandler(sh)

    if _env_truthy("TASK2_LOG_TO_FILE", default=True):
        explicit = (os.environ.get("TASK2_LOG_FILE") or os.environ.get("WEAVIATE_LOG_FILE") or "").strip()
        if explicit:
            log_path = Path(explicit).expanduser()
            log_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            raw_dir = (
                (os.environ.get("TASK2_LOG_DIR") or os.environ.get("WEAVIATE_LOG_DIR") or "").strip()
            )
            log_dir = Path(raw_dir).expanduser() if raw_dir else Path(__file__).resolve().parent.parent / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_path = log_dir / f"{stamp}.log"

        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        base.addHandler(fh)
        base.info("Task2 logging: file=%s", log_path)

    _configured = True


def get_task2_logger(module_name: str) -> logging.Logger:
    """
    Return a child logger under ``task2.*`` so all modules share the same handlers.

    Pass ``__name__`` from each module (e.g. ``main``, ``utils.gpt``, ``agent_a``).
    """
    configure_task2_logging()
    if module_name == "__main__":
        return logging.getLogger(ROOT_LOGGER_NAME)
    if module_name.startswith(f"{ROOT_LOGGER_NAME}."):
        return logging.getLogger(module_name)
    return logging.getLogger(f"{ROOT_LOGGER_NAME}.{module_name}")
