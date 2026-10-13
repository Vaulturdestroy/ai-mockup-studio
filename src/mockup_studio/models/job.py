"""Job + render target models. These are the currency of the pipeline."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    QUEUED = "queued"
    INGESTING = "ingesting"
    PROCESSING = "processing"
    RENDERING = "rendering"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


class RenderTarget(str, Enum):
    FLAT_PNG = "flat_png"
    WEBP = "webp"
    LAYERED_PSD = "layered_psd"
    BLENDER_SCENE = "blender_scene"


class Job(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: JobStatus = JobStatus.QUEUED
    source: str
    product_name: str = "unnamed-product"
    target: RenderTarget = RenderTarget.FLAT_PNG
    style_preset: str = "studio-white"
    seed: int = 0
    output_path: Path | None = None
    error: str | None = None
    attempts: int = 0

    def transition(self, status: JobStatus) -> "Job":
        return self.model_copy(update={"status": status})