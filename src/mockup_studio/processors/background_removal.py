"""Background removal via ONNX segmentation model.

*onnxruntime-directml is the fast path on Windows; falls back to CPU EP if
the DML provider is missing. The model is fetched lazily into
`models/weights/bg_removal.onnx`.*
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from mockup_studio.processors.base import Processor, ProcessorContext
from mockup_studio.utils.log import get_logger

log = get_logger(__name__)

INPUT_SIZE = 1024
ALPHA_THRESHOLD = 0.5


class BackgroundRemovalProcessor(Processor):
    name = "background_removal"
    requires = ("bg_removal.onnx",)

    def __init__(self, weights_dir: Path) -> None:
        self._weights_dir = weights_dir
        self._session = None

    def _load(self):
        if self._session is not None:
            return self._session
        import onnxruntime as ort

        model_path = self._weights_dir / "bg_removal.onnx"
        providers = [p for p in ("DmlExecutionProvider", "CPUExecutionProvider") if p in ort.get_available_providers()]
        log.info("loading bg_removal.onnx with providers=%s", providers)
        self._session = ort.InferenceSession(str(model_path), providers=providers)
        return self._session

    def apply(self, image: Image.Image, ctx: ProcessorContext) -> Image.Image:
        session = self._load()
        resized = image.convert("RGB").resize((INPUT_SIZE, INPUT_SIZE), Image.LANCZOS)
        tensor = np.asarray(resized, dtype=np.float32) / 255.0
        tensor = tensor.transpose(2, 0, 1)[None, ...]

        name = session.get_inputs()[0].name
        mask = session.run(None, {name: tensor})[0][0, 0]
        alpha = (mask > ALPHA_THRESHOLD).astype(np.uint8) * 255
        alpha_img = Image.fromarray(alpha, mode="L").resize(image.size, Image.LANCZOS)

        out = image.convert("RGBA")
        out.putalpha(alpha_img)
        return out