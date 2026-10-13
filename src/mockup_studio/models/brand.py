"""Brand kit + palette models used by the compositor."""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

HEX_LEN = 6


class Palette(BaseModel):
    primary: str = "#1b1b1f"
    secondary: str = "#f5f5f7"
    accent: str = "#ff6a00"
    background: str = "#ffffff"

    @field_validator("primary", "secondary", "accent", "background")
    @classmethod
    def _valid_hex(cls, v: str) -> str:
        raw = v.lstrip("#")
        if len(raw) != HEX_LEN or any(c not in "0123456789abcdefABCDEF" for c in raw):
            raise ValueError(f"bad hex color: {v!r}")
        return f"#{raw.lower()}"


class BrandKit(BaseModel):
    name: str
    palette: Palette = Field(default_factory=Palette)
    logo_path: str | None = None
    font_family: str = "Inter"
    tagline: str | None = None