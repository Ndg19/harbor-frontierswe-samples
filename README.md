# harbor-frontierswe-samples

Three Harbor-format tasks (heat sensitivities, CBOR framing, log forensics).

| Task | Folder |
|------|--------|
| Heat event sensitivities | [tasks/adjoint-heat-events](tasks/adjoint-heat-events) |
| Slotted CBOR framing | [tasks/slotted-cbor-framing](tasks/slotted-cbor-framing) |
| Auth-chain forensics | [tasks/auth-chain-forensics](tasks/auth-chain-forensics) |

RustLabs sample brief: [docs/client/forms.md](docs/client/forms.md)

```bash
python3 frontierswe-check.py tasks/<name>
harbor run -p tasks/<name> -a oracle -y --job-name my-oracle-run
harbor run -p tasks/<name> -a nop -y --job-name my-nop-run
```

Use a new `--job-name` each Harbor run.

Nigusie Dessalegn — kingniguse81@gmail.com
