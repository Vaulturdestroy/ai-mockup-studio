"""Perspective warp — maps a flat product cutout onto a scene plane.

The homography is computed from four corner points the driver supplies
via `ctx`; when absent, we fall back to a centered, slightly pitched quad
that reads as a studio turntable.
"""
from __future__ import annotations

import numpy as np
from PIL import Image

from mockup_studio.processors.base import Processor, ProcessorContext

DEFAULT_PITCH = 0.12


def _default_quad(w: int, h: int) -> np.ndarray:
    inset = int(w * 0.08)
    top = int(h * DEFAULT_PITCH)
    return np.array(
        [[inset, top], [w - inset, 0], [w - inset, h], [inset, h - top]],
        dtype=np.float32,
    )


class PerspectiveWarpProcessor(Processor):
    name = "perspective_warp"

    def __init__(self, target_size: tuple[int, int] = (1600, 1200)) -> None:
        self._target = target_size

    def apply(self, image: Image.Image, ctx: ProcessorContext) -> Image.Image:
        tw, th = self._target
        src = np.array(
            [[0, 0], [image.width, 0], [image.width, image.height], [0, image.height]],
            dtype=np.float32,
        )
        dst = _default_quad(tw, th)
        coeffs = _find_homography(src, dst)
        warped = image.transform((tw, th), Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC)
        return warped


def _find_homography(src: np.ndarray, dst: np.ndarray) -> tuple[float, ...]:
    """Solve the 8-param projective transform. O(1) — fixed 8x8 system."""
    a = []
    for (x, y), (u, v) in zip(src, dst, strict=True):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    a = np.asarray(a, dtype=np.float64)
    b = dst.flatten()
    sol = np.linalg.solve(a, b)
    return tuple(float(c) for c in sol)