# Contributing to ai-mockup-studio

Thanks for wanting to make mockups less painful. This repo is a pipeline:
**ingest -> process -> render -> output**. If your change crosses a stage
boundary, say so in the PR description.

## Dev setup

```bash
git clone https://github.com/ai-mockup-studio/ai-mockup-studio
cd ai-mockup-studio
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
python -m mockup_studio doctor
```

`doctor` prints your detected backends: `onnxruntime` (CPU/CUDA/DirectML),
`torch` (fallback), `Pillow`, and whether the SDXL-turbo mockup pack is
cached under `models/weights/`.

## Where things live

- `src/mockup_studio/ingest/` — pull raw product photos, spec sheets, and
  brand kits off disk, clipboard, or a URL. Handlers must be idempotent.
- `src/mockup_studio/processors/` — background removal, perspective warp,
  lighting harmonization, label compositing.
- `src/mockup_studio/drivers/` — output formats: PNG, WebP, layered PSD,
  and a Blender scene stub.
- `src/mockup_studio/jobs/` — the queue, worker pool, and retry policy.

## Adding a new output driver

1. Subclass `drivers.base.OutputDriver`.
2. Implement `render(job, canvas) -> Path`.
3. Register it in `drivers/registry.py`.
4. Add a fixture under `tests/fixtures/` and a test in
   `tests/test_drivers.py`.

## Adding a new ingest source

Subclass `ingest.base.IngestHandler`, implement `pull(source) -> IngestResult`.
Return `IngestResult.skipped(reason)` instead of raising when the source is
empty — the pipeline treats skipped as a non-fatal outcome.

## Style

- `ruff` + `black`, line length 100.
- Type hints required on public functions.
- No `print()` in library code — use `mockup_studio.utils.log.get_logger`.
- Windows-first: paths go through `pathlib`, never string concat.

## Commit messages

`ingest:`, `processor:`, `driver:`, `job:`, `cli:`, `docs:`, `fix:`.

## PR checklist

- [ ] `pytest -q` passes
- [ ] `ruff check src tests` clean
- [ ] New driver/handler has a fixture + test
- [ ] `CHANGELOG.md` entry under `## Unreleased`