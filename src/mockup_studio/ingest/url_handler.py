"""URL ingest. Follows redirects up to MAX_REDIRECTS and pins schemes.

*httpx follows redirects by default; cap them here instead of trusting the
library default (10) so a hostile redirect chain can't stall a worker.*
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import httpx

from mockup_studio.config.settings import Settings
from mockup_studio.ingest.base import IngestHandler, IngestResult
from mockup_studio.utils.log import get_logger

log = get_logger(__name__)

USER_AGENT = "ai-mockup-studio/0.6 (+https://github.com/ai-mockup-studio)"


class UrlIngestHandler(IngestHandler):
    name = "url"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def pull(self, source: str) -> IngestResult:
        parsed = urlparse(source)
        if parsed.scheme not in self._settings.allowed_schemes:
            return IngestResult.skipped(source, f"scheme not allowed: {parsed.scheme!r}")

        dest_dir = self._settings.cache_dir / "ingest" / "url"
        dest_dir.mkdir(parents=True, exist_ok=True)
        filename = Path(parsed.path).name or "download"
        dest = dest_dir / filename

        try:
            with httpx.Client(
                follow_redirects=True,
                max_redirects=self._settings.max_redirects,
                timeout=20.0,
                headers={"User-Agent": USER_AGENT},
            ) as client:
                resp = client.get(source)
                resp.raise_for_status()
        except httpx.HTTPError as exc:
            log.warning("url ingest failed for %s: %s", source, exc)
            return IngestResult.skipped(source, f"http error: {exc}")

        dest.write_bytes(resp.content)
        return IngestResult.success(source, [dest], kind="url", content_type=resp.headers.get("content-type"))