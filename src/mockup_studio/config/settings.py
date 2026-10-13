"""Runtime settings for the mockup pipeline.

Env vars are prefixed `MOCKUP_STUDIO_`. Anything not set falls back to
the Windows-friendly defaults in `DEFAULTS`.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

Backend = Literal["directml", "cuda", "cpu", "torch"]


@dataclass(frozen=True, slots=True)
class Settings:
    workdir: Path
    outputs_dir: Path
    cache_dir: Path
    weights_dir: Path
    backend: Backend
    workers: int
    max_redirects: int
    allowed_schemes: tuple[str, ...]
    blender_bin: str | None
    strict: bool
    log_level: str = "INFO"
    extra: dict[str, str] = field(default_factory=dict)

    def ensure_dirs(self) -> None:
        for d in (self.outputs_dir, self.cache_dir, self.weights_dir):
            d.mkdir(parents=True, exist_ok=True)


DEFAULTS: dict[str, str] = {
    "BACKEND": "directml",
    "WORKERS": "0",  # 0 -> auto (os.cpu_count() capped at 8)
    "MAX_REDIRECTS": "3",
    "ALLOWED_SCHEMES": "http,https",
    "LOG_LEVEL": "INFO",
}


def _env(name: str) -> str | None:
    return os.environ.get(f"MOCKUP_STUDIO_{name}")


def load_settings(workdir: Path | None = None) -> Settings:
    root = Path(workdir or Path.cwd()).resolve()
    strict = _env("STRICT") == "1"

    backend: Backend = _env("BACKEND") or DEFAULTS["BACKEND"]  # type: ignore[assignment]
    workers_raw = int(_env("WORKERS") or DEFAULTS["WORKERS"])
    workers = workers_raw or min(os.cpu_count() or 4, 8)

    schemes = tuple(
        s.strip()
        for s in (_env("ALLOWED_SCHEMES") or DEFAULTS["ALLOWED_SCHEMES"]).split(",")
        if s.strip()
    )
    if strict:
        schemes = tuple(s for s in schemes if s in {"http", "https"})

    blender = None if strict else _env("BLENDER_BIN")

    return Settings(
        workdir=root,
        outputs_dir=root / "outputs",
        cache_dir=root / ".mockup_cache",
        weights_dir=root / "models" / "weights",
        backend=backend,
        workers=workers,
        max_redirects=int(_env("MAX_REDIRECTS") or DEFAULTS["MAX_REDIRECTS"]),
        allowed_schemes=schemes,
        blender_bin=blender,
        strict=strict,
        log_level=_env("LOG_LEVEL") or DEFAULTS["LOG_LEVEL"],
    )