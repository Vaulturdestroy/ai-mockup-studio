"""Composite label text + brand color onto the product surface."""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from mockup_studio.processors.base import Processor, ProcessorContext

FALLBACK_FONT = "segoeui.ttf"  # Windows default; falls back to PIL's bitmap font


class LabelCompositor(Processor):
    name = "label_compositor"

    def __init__(self, label_text: str | None = None, font_size: int = 48) -> None:
        self._label = label_text
        self._font_size = font_size

    def apply(self, image: Image.Image, ctx: ProcessorContext) -> Image.Image:
        if not self._label:
            return image
        out = image.convert("RGBA")
        draw = ImageDraw.Draw(out)
        try:
            font = ImageFont.truetype(FALLBACK_FONT, self._font_size)
        except OSError:
            font = ImageFont.load_default()

        accent = (ctx.brand_palette or {}).get("accent", "#ff6a00")
        bbox = draw.textbbox((0, 0), self._label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (out.width - tw) // 2
        y = int(out.height * 0.72)
        pad = 18
        draw.rounded_rectangle(
            [x - pad, y - pad, x + tw + pad, y + th + pad],
            radius=16,
            fill=accent,
        )
        draw.text((x, y), self._label, font=font, fill="#ffffff")
        return out