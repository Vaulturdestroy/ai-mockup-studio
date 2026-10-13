# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Email `security@ai-mockup-studio.dev` with a description, repro steps, and
the output of `python -m mockup_studio doctor --json`. Please do not open a
public issue for anything that could be used to exfiltrate a user's product
photos or brand assets.

## Threat model

ai-mockup-studio is a local-first desktop tool. It:

- reads product photos, spec sheets, and brand kits from paths the user
  explicitly provides;
- optionally fetches a reference image from a URL when the user pastes one;
- writes renders to `outputs/` inside the user's working directory;
- caches model weights under `models/weights/`.

Out of scope for this tool: network listening, privilege escalation, and
anything that would let a mockup job read files the user didn't point at.

### Known sharp edges

- `ingest.url_handler` follows redirects. If you expose it to untrusted
  input, cap `MAX_REDIRECTS` and pin `ALLOWED_SCHEMES` to `{http, https}`.
- The Blender driver shells out to a user-provided `blender` binary. Keep
  `BLENDER_BIN` on a trusted path.
- PSD export writes a zip container; sanitize layer names before export if
  your pipeline ingests untrusted text.

## Hardening

Run with `MOCKUP_STUDIO_STRICT=1` to disable URL ingest and the Blender
driver in one shot.