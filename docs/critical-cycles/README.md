# The Critical-Cycle Index (N-Series)

**Receipted human-in-the-loop critical resolutions in autonomous self-healing infrastructure.**

This folder is the live, append-only index of every completed **critical-cycle**: a full governance loop in which an autonomous infrastructure detects a critical-severity anomaly, **holds** (refuses to auto-heal), requires a human acknowledgment (ACK) from the system's owner, heals under an exact-matching playbook, and resolves with a complete audit trail. The human step is never automated — that is the point.

## Why it exists

Autonomous-settlement and self-healing claims are cheap. Receipts are not. Each entry below is a timestamped, checksummed, DOI-published record of governed autonomy: the machine asked permission before it touched a critical path, a human answered, and the whole exchange is preserved for audit.

## The Index

| # | Cycle | Date | Substrate | DOI | Receipt |
|---|-------|------|-----------|-----|---------|
| 1 | **N10-ACK** — first receipted HITL critical resolution (PQC keyring desync, critical bait) | Oct 4, 2026 | Lineage box (hand-built) | [10.5281/zenodo.23151356](https://doi.org/10.5281/zenodo.23151356) | Zenodo record |
| 2 | **N-D1-ACK** — first HITL critical on a zero-lineage stamped box (legacy ECDSA-P256 detection, migration to CRYSTALS-Dilithium3) | Oct 7, 2026 | Stamped box (standard v1.1 template, SIM-D) | [10.5281/zenodo.23217495](https://doi.org/10.5281/zenodo.23217495) | [ND1_ACK_RECEIPT.md](ND1_ACK_RECEIPT.md) |

*New entries are appended as cycles complete. Entries are never edited or removed — errors are corrected by disclosed amendment only.*

## The loop every entry must complete

```
DETECT → HOLD (Rule 2: no auto-heal on critical crypto ops)
       → CONSTITUTIONAL CHECK (Articles I–III)
       → HUMAN ACK (owner, escalation channel)
       → HEAL (exact-type playbook match only)
       → RESOLVE (alerts closed per ACK protocol, Pattern + LearningMetric logged)
```

## Verification

- Every cycle's full trail lives in the [append-only daily ledger](../../RUN/DAILY_LEDGER.md)
- The 60-day Horsemen benchmark (Oct 7 – Dec 6, 2026) that generates ongoing chaos-cycle data is preregistered at [github.com/LLong2026/four-horsemen](https://github.com/LLong2026/four-horsemen)
- Substrate determinism receipts (SDR series) live in [docs/sim-d/](../sim-d/) and the research folders

## Disclosure

All critical-cycle anomaly data is **synthetic** (simulated attack material on sealed synthetic rails; zero real key material, wallets, or production crypto is ever involved). The detection, containment, governance, healing, and audit machinery is real and receipted. This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.
