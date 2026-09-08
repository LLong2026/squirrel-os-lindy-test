# LINDY TEST — 30-DAY FIRST RUN (1st Run)

**Run window: September 7, 2026, 7:00 PM CT → October 7, 2026**
**Objective: 30 consecutive days of continuous, self-healing, human-hands-off operation.**

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

## What This Is

The Lindy Test is the credibility benchmark for SQUIRL OS: a 30-day continuous run of the entire ecosystem — heartbeat monitoring, chaos training ramp (Mon/Wed/Fri 11pm CT), technician reconciliation (7am/7pm CT), records syncs, weekly audits — with the configuration FROZEN. No new features, no hotfixes mid-run. Whatever doesn't survive gets fixed AFTER the run, and the failure itself becomes learning material.

The test answers one buyer question: *does this thing actually run itself?*

## Downtime Definition (Honest Standard)

A day is marked **DOWN** if any of:
1. A scheduled run misses its window (chaos, reconciliation, records sync, bill watch)
2. System health drops below OPERATIONAL between scans
3. An incident requires Leon's hands (human intervention = crack in the log)

**Self-healed incidents are WINS, not downtime.** Every anomaly detected, healed, and learned from without human touch is the product working — and is logged honestly. A 30-day ledger with a dozen self-healed incidents in it is MORE credible than a suspiciously clean one.

## Folder Contents

| File | Purpose |
|---|---|
| `DAILY_LEDGER.md` | One entry per day: uptime verdict, checkpoints, incidents (win/down), one-line status |
| `LEARNING_LOG.md` | Every pattern, defect, and observation the run surfaces — the self-learning loop, written down |
| `BENCHMARK_LINDY_30_FINAL.md` | The formal benchmark document, written at run close (Oct 7) if the test holds |

## Operating Rules During the Run

- STABILIZATION FREEZE holds: no builder messages, no code edits, no schema/workflow changes
- Checkpoints piggyback existing scheduled workflows — zero added credit cost
- Human-in-the-loop approvals (cages, ACKs, SIPs, canary) proceed as normal — those ARE the system working
- Any worthy milestone during the run gets marketed from REAL entity data only
- Leon monitors: Tecnichain (tickets), Hypervisor (anomaly view — mirror is display-only), Gabriel chat (escalations/ACKs), corporate email (reports). Everything else is the machine's side of the glass.

## Ownership & License

SQUIRL OS Technologies LLC — Leon Calvin Long II. 7 patents pending + 5 SBIR tracks. Prototype license: USE rights only.
