"""Layered PSD driver — writes a minimal PSD-compatible zip container.

*Real PSD is a proprietary binary format; we emit a zip of flattened +
per-layer PNGs and a manifest.json. Photoshop opens the flattened layer;
advanced users can rebuild the stack from the manifest.*
"""
from __future__ import annotations

import json
import zipfile
from io import BytesIO
from pathlib import Path

from