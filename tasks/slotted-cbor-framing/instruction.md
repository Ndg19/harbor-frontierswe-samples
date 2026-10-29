`/app/repo` already exposes a small CBOR codec (maps with UTF-8 keys, byte-string values, plus basic text and integers). Services now need a framed transport on top so records can be multiplexed over pipes and sockets without losing framing.

Implement version 1 from `/app/FRAMING_SPEC.md`.

## Deliverables

1. **Framing module** in `/app/submission/slotted_cbor`, keeping the existing `encode_map` / `decode_map` API unchanged for callers that only need CBOR.

2. **CLI** via `python -m slotted_cbor`:
   - `encode --manifest PATH --output PATH` — read a JSON manifest (`slot`, `name`, `path` relative to the manifest directory), reject duplicate slots, write a framed stream.
   - `decode --input PATH --output-dir PATH` — verify Castagnoli CRC32C per frame, enforce unique slots, reject trailing garbage.
   - `stream-decode --input PATH` — one JSON line per frame on stdout (`slot`, `name`, `body_hex`).

3. **Error handling.** Truncated input, CRC failures, duplicate slot IDs, and trailing bytes after the last frame exit with the codes documented in the spec (`SLCB:<code>:...` on stderr).

Example corpus under `/app/data/` is for local testing; do not modify those files.
