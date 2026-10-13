"""Spec-sheet ingest — parses product JSON/YAML into a ProductSpec.

Kept separate from file ingest so a spec-only job (no photo) can still
drive a mockup from the compositor's generated silhouette.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from mockup_studio.ingest.base import IngestHandler, IngestResult
from mockup_studio.models.product import ProductCategory, ProductSpec
from mockup_studio.utils.log import get_logger

log = get_logger(__name__)


class SpecSheetHandler(IngestHandler):
    name = "spec"

    def pull(self, source: str) -> IngestResult:
        path = Path(source)
        if not path.exists() or path.suffix.lower() not in {".json", ".yaml", ".yml"}:
            return IngestResult.skipped(source, "not a json/yaml spec sheet")

        raw = path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw) if path.suffix.lower() in {".yaml", ".yml"} else json.loads(raw)

        try:
            spec = ProductSpec(
                name=data["name"],
                category=ProductCategory(data.get("category", "other")),
                width_mm=data.get("width_mm"),
                height_mm=data.get("height_mm"),
                depth_mm=data.get("depth_mm"),
                material=data.get("material"),
                label_text=data.get("label_text"),
                notes=list(data.get("notes", [])),
            )
        except (KeyError, ValueError) as exc:
            return IngestResult.skipped(source, f"bad spec sheet: {exc}")

        return IngestResult.success(source, [path], kind="spec", spec=spec.model_dump())