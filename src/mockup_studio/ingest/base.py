"""Base ingest handler. All handlers return IngestResult; none raise on
empty input — the pipeline treats 'skipped' as a first-class outcome.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class IngestResult:
    ok: bool
    source: str
    artifacts: list[Path] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    skipped_reason: str | None = None

    @classmethod
    def skipped(cls, source: str, reason: str) -> "IngestResult":
        return cls(ok=False, source=source, skipped_reason=reason)

    @classmethod
    def success(cls, source: str, artifacts: list[Path], **meta: Any) -> "IngestResult":
        return cls(ok=True, source=source, artifacts=artifacts, metadata=meta)


class IngestHandler(ABC):
    """Idempotent puller of raw product input."""

    name: str = "base"

    @abstractmethod
    def pull(self, source: str) -> IngestResult: ...