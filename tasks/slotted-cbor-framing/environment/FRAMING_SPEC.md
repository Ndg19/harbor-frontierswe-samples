# Slotted CBOR framing (version 1)

## File envelope

Every framed stream begins with the 5-byte header `SLCB\x01` (magic + version).

## Frames

After the header, zero or more frames appear:

| Field | Size | Description |
|-------|------|-------------|
| slot | 4 | big-endian uint32 slot identifier (must be unique within a stream) |
| length | 4 | big-endian uint32 payload length N |
| crc32c | 4 | big-endian CRC32C (Castagnoli) of the next N bytes |
| payload | N | CBOR map encoded with repo `cbor.encode_map` |

Payload maps must contain exactly keys `name` (UTF-8 text) and `body` (byte string). Values are copied verbatim from manifest files during encode.

## Error codes

CLI commands exit non-zero and print `SLCB:<code>:<message>` to stderr:

| Code | Meaning |
|------|---------|
| 2 | truncated stream / incomplete frame |
| 3 | CRC mismatch |
| 4 | trailing bytes after last frame |
| 5 | duplicate slot id |

## Manifest JSON

Array of objects `{ "slot": int, "name": str, "path": str }`. Paths are relative to the manifest directory. Slots must be unique.

## Streaming

`stream-decode` reads from the input file through a stream interface (no requirement to load the entire file before parsing the first frame). It must emit one JSON object per completed frame: `{ "slot": int, "name": str, "body_hex": str }`. Incomplete frames, bad CRC, duplicate slots, and trailing bytes after the last frame use the same error codes as `decode`.
