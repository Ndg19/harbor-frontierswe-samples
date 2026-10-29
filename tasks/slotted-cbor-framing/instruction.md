The repository under `/app/repo` ships a **restricted CBOR** encoder and decoder for maps with UTF-8 string keys and byte-string values, plus small integers and text. Downstream transport needs a **slotted framing layer** so multiplexed records can be streamed safely over pipes and sockets.

Read `/app/FRAMING_SPEC.md` and implement the framing protocol on top of the existing CBOR subset. Deliver an importable package at `/app/submission/slotted_cbor` exposing the same CBOR API and new framing helpers, plus a module CLI:

- `python -m slotted_cbor encode --manifest PATH --output PATH`
- `python -m slotted_cbor decode --input PATH --output-dir PATH`
- `python -m slotted_cbor stream-decode --input PATH` (write one JSON line per frame to stdout)

Encoding must read a JSON manifest listing `{ "slot": int, "name": str, "path": str }` entries relative to the manifest directory, wrap each payload as specified, and reject duplicate slot identifiers. Decoding must verify **Castagnoli CRC32C** per frame, enforce unique slots, refuse ambiguous trailing bytes, and surface stable error codes from the spec. Streaming decode must tolerate partial reads without losing synchronization after a complete frame.

Bundled corpora live under `/app/data/` for local development. Hidden verification uses additional mutation streams (truncated frames, bad CRC, duplicate slots, oversized length fields). A full pass requires every probe to succeed; partial credit is not awarded.

Do not modify files under `/app/data`. Keep the CBOR subset backward compatible for callers that only import encode/decode map helpers.
