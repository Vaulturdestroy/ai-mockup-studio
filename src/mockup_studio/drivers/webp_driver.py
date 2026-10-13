"""WebP driver — optimized for marketplace listings."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from mockup_studio.drivers.base import OutputDriver
from mockup_studio.models.job import Job


class WebpDriver(OutputDriver):
    name = "webp"
    extension = ".webp"

    def __init__(self, outputs_dir: Path, quality: int = 88) -> None:
        self._outputs = outputs_dir
        self._quality = quality

    def render(self, job: Job, canvas: Image.Image) -> Path:
        self._outputs.mkdir(parents=True, exist_ok=True)
        dest = self._outputs / f"{job.product_name}-{job.id}{self.extension}"
        canvas.save(dest, format="WEBP", quality=self._quality, method=6)
        return dest