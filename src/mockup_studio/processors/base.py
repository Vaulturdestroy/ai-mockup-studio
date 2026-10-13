"""Processor base class. Processors are pure-ish: input image in, output
image out, no disk writes. The orchestrator handles I/O.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from PIL import Image


@dataclass(slots=True)
class ProcessorContext:
    job_id: str
    style_preset: str
    seed: int
    brand_palette: dict[str, str] | None = None


class Processor(ABC):
    name: str = "base"
    requires: tuple[str, ...] = ()

    @abstractmethod
    def apply(self, image: Image.Image, ctx: ProcessorContext) -> Image.Image: ...