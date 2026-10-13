"""Output driver base. A driver turns a rendered canvas into a file on
disk (or a scene stub) and returns the path it wrote.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

from mockup_studio.models.job import Job


class OutputDriver(ABC):
    name: str = "base"
    extension: str = ".bin"

    @abstractmethod
    def render(self, job: Job, canvas: Image.Image) -> Path: ...