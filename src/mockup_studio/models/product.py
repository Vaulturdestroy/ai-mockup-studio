"""Product spec model — what the ingest stage produces and processors consume."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ProductCategory(str, Enum):
    BOTTLE = "bottle"
    BOX = "box"
    POUCH = "pouch"
    CAN = "can"
    JAR = "jar"
    TUBE = "tube"
    DEVICE = "device"
    GARMENT = "garment"
    OTHER = "other"


class ProductSpec(BaseModel):
    name: str
    category: ProductCategory = ProductCategory.OTHER
    width_mm: float | None = None
    height_mm: float | None = None
    depth_mm: float | None = None
    material: str | None = None
    label_text: str | None = None
    notes: list[str] = Field(default_factory=list)

    @property
    def aspect(self) -> float | None:
        if self.width_mm and self.height_mm:
            return self.width_mm / self.height_mm
        return None