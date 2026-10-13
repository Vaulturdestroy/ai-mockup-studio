"""Local filesystem ingest — the common case on Windows."""
from __future__ import annotations

from pathlib import Path

from mockup_studio.ingest.base import IngestHandler, IngestResult
from mockup_studio.utils.log import get_logger

log = get_logger(__name__)

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
SPEC_EXTS = {".json", ".yaml", ".yml", ".toml", ".csv", ".txt"}


class FileIngestHandler(IngestHandler):
    name = "file"

    def pull(self, source: str) -> IngestResult:
        path = Path(source).expanduser()
        if not path.exists():
            return IngestResult.skipped(source, f"path does not exist: {path}")

        if path.is_dir():
            artifacts = [
                p for p in sorted(path.iterdir()) if p.suffix.lower() in IMAGE_EXTS | SPEC_EXTS
            ]
            if not artifacts:
                return IngestResult.skipped(source, "directory had no supported files")
            log.info("ingested %d files from %s", len(artifacts), path)
            return IngestResult.success(source, artifacts, kind="directory")

        if path.suffix.lower() not in IMAGE_EXTS | SPEC_EXTS:
            return IngestResult.skipped(source, f"unsupported extension: {path.suffix}")

        return IngestResult.success(source, [path], kind="file")