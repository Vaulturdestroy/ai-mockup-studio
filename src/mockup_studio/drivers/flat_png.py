"""Flat PNG driver — the default output."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from mockup_studio.drivers.base import OutputDriver
from mockup_studio.models.job import Job


class FlatPngDriver(OutputDriver):
    name = "flat_png"
    extension = ".png"

    def __init__(self, outputs_dir: Path) -> None:
        self._outputs = outputs_dir

    def render(self, job: Job, canvas: Image.Image) -> Path:
        self._outputs.mkdir(parents=True, exist_ok=True)
        dest = self._outputs / f"{job.product_name}-{job.id}{self.extension}"
        canvas.save(dest, format="PNG", optimize=True)
        return dest