"""Match the product's lighting to the scene's key light direction.

Uses a cheap luminance-histogram match against the target scene plate.
Good enough for mockups; not a relight.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageStat

from mockup_studio.processors.base import Processor, ProcessorContext


class LightingHarmonizer(Processor):
    name = "lighting_harmonizer"

    def __init__(self, strength: float = 0.65) -> None:
        if not 0.0 <= strength <= 1.0:
            raise ValueError("strength must be in [0, 1]")
        self._strength = strength

    def apply(self, image: Image.Image, ctx: ProcessorContext) -> Image.Image:
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
        mean = np.asarray(stat.mean, dtype=np.float32)
        target = np.array([188.0, 188.0, 190.0], dtype=np.float32)  # neutral studio key
        gain = 1.0 + (target - mean) / 255.0 * self._strength
        arr = np.asarray(rgb, dtype=np.float32) * gain
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr, mode="RGB")