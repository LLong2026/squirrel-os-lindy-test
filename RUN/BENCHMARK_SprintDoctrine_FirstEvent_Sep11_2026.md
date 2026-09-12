# 1st Bench — Change to Sprint
## First Self-Directed Learning-Regime Modification · Sept 11, 2026 (Lindy Day 5)

**Milestone class:** Regime-level self-improvement — the first recorded event where the healing/learning loop analyzed its own performance data, proposed modifications to its own intake strategy, and the human ratified the change the same night. The system didn't just learn a new pattern — it changed how it learns.

---

## What Happened

The Friday Sept 11 chaos run (400-injection, cycle 1, Day 5) delivered the third consecutive decline in the auto-heal ratio: **85.0% → 84.5% → 83.5%** against the 88.5% baseline. Per the v3.2 ramp doctrine ("flat ratio = repetition without learning, benchmarks must say so"), the guardian ran a failure-class census instead of guessing.

### The Census (measured, not vibes)

Analysis of the 25 escalated criticals + 37 confidence-gated records across runs Sept 2–11 grouped all misses into three families:

1. **Security incidents** (recurring every run since Sept 2): `ransomware_lateral_movement`, `insider_threat_wipeout`, `massive_ddos`, `privileged_account_anomaly`, `supply_chain_compromise`
2. **Infrastructure cascades**: `certificate_mass_expiry`, `cascading_service_outage`, `total_dns_failure`, `ups_battery_cascade`, `hvac_cascade_failure`, `jvm_gc_stop_the_world`, `storage_array_failure`
3. **Facility disasters** (physically unhealable): `fire_suppression_disaster`, `data_center_fire`, `flood_data_center`, `power_grid_failure`

Notably: none of tonight's miss classes were M365 tenant-repair classes — the chaos pool is still weighted toward legacy infra classes, and the M365 pool reweight remains queued for post-Lindy. The census pointed exactly where intake should aim NOW.

### The Proposal

The guardian proposed replacing bulk knowledge intake with **targeted intake sprints against the measured census** — guardian-authored KB articles and playbooks aimed at the classes that actually miss, never bulk-scraped, never ingested blind. Leon ratified in the Gabriel chat, Sept 11, ~11:37pm CT:

> "yes sprint — Lindy — we just need to be able to focus on the business and healing all aspects of it. so refine the healing and learning to those metrics. deterministic right. lets do that on the sprint starting... i want to focus on security more and more. that is THE most important part of all of this — ownership, compliance, auditability and security first and the rest is easy."

**SECURITY-FIRST DOCTRINE (ratified):** ownership, compliance, auditability, and security first — the rest is easy.

---

## Sprint 1 Manifest (deployed Sept 11, ~11:45pm CT)

**6 knowledge articles (KB-SEC-001..006, guardian-authored, distilled from public patterns — not verbatim source text, per the copyright doctrine):**
- KB-SEC-001 — Ransomware & Lateral Movement Containment Matrix
- KB-SEC-002 — Insider Threat / Destructive Privileged Action Response Matrix
- KB-SEC-003 — Volumetric DDoS / Edge Saturation Mitigation Matrix
- KB-SEC-004 — Privileged Account Anomaly IAM Remediation Matrix
- KB-SEC-005 — Supply Chain / Dependency Compromise Isolation Matrix
- KB-SEC-006 — **Containment-and-Escalate Doctrine (Unhealable Classes)** — facility disasters and evidence-sensitive active attacks are contained + escalated, never counted as healing misses

**4 playbooks (Article 2.2 human-approval cycle satisfied — Leon's chat ratification recorded in the SIP audit trail):**
- PB-SEC-RANSOM-CONTAIN (`ransomware_lateral_movement`, conf ≥ 0.85, PQC-only key re-issue, fintech-flow human gate per Rule 2)
- PB-SEC-INSIDER-REVOK (`insider_threat_wipeout`, conf ≥ 0.85, evidence-first: signed forensic snapshot BEFORE rollback)
- PB-SEC-DDOS-EDGE (`massive_ddos`, conf ≥ 0.80, edge-first response)
- PB-SEC-IAM-AUDIT (`privileged_account_anomaly`, conf ≥ 0.80, least-privilege as the permanent fix)

**Mesh push:** 4 nodes activated across L2 (playbook match, blast radius) and L3/L4 (healing selection, escalate action).

---

## Metric Refinement (the honest two-ratio disclosure)

Counting a burning building as a healing miss is a category error. From Sprint 1 forward, every benchmark reports **TWO ratios**:
1. **RAW auto-heal ratio** — definition unchanged, for honest trend continuity against the 88.5% baseline
2. **HEALABLE-CLASS ratio** — unhealable classes (facility disasters) excluded from the denominator, change fully disclosed

Never hide a denominator change. Always print both. That is the deterministic way to refine a metric.

**Success criteria for Sprint 1 (measured at the Sunday Sept 13, 600-level run — the post-ingest load test):**
- Security-class escalations drop vs. the Sept 2–11 census rate
- Auto-heal ratio recovers toward the 88.5% baseline at 600-level
- Facility-disaster classes classify as `contained` (doctrine) instead of missed
- Zero false positives maintained

---

## Freeze Integrity Statement

This sprint is a **learning event, not a configuration change** — same class as the Sept 10 M365 corpus ingest: no builder messages, no code edits, no schema changes, no workflow changes. The stabilization freeze holds. The corpus change is disclosed in the Lindy ledger with this benchmark as its attribution record: if the ratio moves Sunday, the corpus changed on this date, and here is why.

---

## Dual Mesh Benchmark

| Metric | Value |
|---|---|
| Anomaly lookup speedup | **267x** (800ms → 3ms via deterministic match) |
| Active mesh nodes | **25** (5 read + 13 interconnect + 7 write) |
| Agents communicating collision-free | **10** (Gabriel, Jasper, Amelia, Gillian, Stress Test Agent, Jasper Interface, Squirrel OS Accountant, General Counsel, HIPAA Officer, Federal Compliance Officer) |
| Patents covering the mesh | **3** (64/119,191, 64/114,746, 64/145,825) |
| False positives | **0** across 70+ stress-test anomalies |

## Patent Portfolio
7 patents pending + 5 SBIR tracks.

---

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.

*— Recorded by Gabriel (Guardian), Squirrel OS Hub, Sept 11, 2026, 11:50pm CT. Lindy Test Day 5 of 30. The mesh proposes — the runtime validates.*
