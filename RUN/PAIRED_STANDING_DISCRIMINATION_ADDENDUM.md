# Paired Standing-Discrimination Records — Addendum A

**Published:** September 16, 2026 (additive documentation; no run data modified)
**Responds to:** a public examiner's request for the exact paired records constituting the claimed standing-discrimination property — same unchanged implementation, standing-preserving ΔN → execute, standing-defeating ΔN → refuse, against the same consequential boundary.
**Source record:** the Sept 7, 2026 LVR-0907 gauntlet, 200 anomalies, frozen public snapshot at commit `28c07be` (sheet "LVR-0907 DETAIL (200)" in `RUN/SQUIRL_OS_INCIDENT_LEDGER.xlsx`); same-night 400-level validation at commit `07cd230`. This addendum was compiled September 16 from the server-side records; the September 7–8 snapshot is untouched.

---

## 1. Implementation & Version Identity

- **Runtime:** SQUIRL OS Hub — deterministic validation layer over a probabilistic detection mesh (mesh proposes, runtime validates). Base44 instance `69b57683f2623117603736bc` (SQUIRL OS Hub), Lindy 30-Day 1st Run configuration.
- **Run window:** 2026-09-07T15:10:00Z (single batch; every row in the annex carries this detection timestamp).
- **Configuration timeline (stated plainly):** the LVR-0907 gauntlet was the Day 1 baseline capture under the standing configuration. The Lindy charter (private repo commit `303e73a`, Sept 7, 7:55 PM CT) froze that exact configuration for the 30-day run beginning 7:00 PM CT; the same frozen configuration was validated unchanged at the 11:00 PM CT chaos run (public commit `07cd230`). No repair, tuning, or threshold change between the baseline capture, the freeze, and the night run.
- **The gate (unchanged across all cases):** a state-changing healing action executes only when ALL of:
  1. an exact-type playbook exists for the detected anomaly (exact-match-only rule), and
  2. detection confidence ≥ that playbook's frozen `confidence_threshold` (per-playbook, not flat), and
  3. the flow is not protected/critical — critical-severity detections route to mandatory human disposition regardless of confidence.
  Standing not established → **no execution**: the anomaly holds as `detected` and is flagged for review. No retry, no stale authority.

## 2. Prospective Acceptance Criterion

The acceptance criteria for the pair are the playbook definitions themselves — each carries a frozen `confidence_threshold` and trigger condition, immutable during execution (operating rule: playbooks never modified at runtime). The falsifier is symmetric and mechanical: **any sub-threshold execution, or any above-threshold refusal without a protected-flow reason, falsifies the claim.** Both branch outcomes were recorded and committed publicly on Sept 8 (`28c07be`), before any external review.

## 3. The Featured Pair — same run window, same gate, opposite dispositions

### RECORD A — standing preserved → EXECUTE
**Ticket:** `LVR-0907-011` — `quantum_entropy_source_depletion` (PQC domain), severity: high (per the frozen annex)

| Stage | Record |
|---|---|
| T₀ (authority/state) | System OPERATIONAL, health 100/100; standing configuration with exact-type playbook present |
| ΔN (the change) | Anomaly injected; detection confidence **0.71** |
| Tₙ (standing check) | Exact-type playbook "Quantum Entropy Source Depletion Remediation", frozen threshold **0.70**. 0.71 ≥ 0.70 → **standing established → execute** |
| Consequence trace | Playbook bound to the server-side anomaly record (`linked_playbook_id` populated); heal executed; pattern reinforcement applied; annex row `resolved` at commit `28c07be`. Batch healing events are timestamped playbook-group records; per-ticket linkage is preserved on the anomaly record |

### RECORD B — standing defeated → REFUSE
**Ticket:** `LVR-0907-022` — `wildfire_camera_smoke_false`, severity: high

| Stage | Record |
|---|---|
| T₀ (authority/state) | Same run window, same frozen configuration, same gate |
| ΔN (the change) | Anomaly injected; detection confidence **0.708** |
| Tₙ (standing check) | Exact-type playbook PB-C81 exists, frozen threshold **0.85**. 0.708 < 0.85 → **standing NOT established → do not execute** |
| Consequence trace | No playbook bound, **no healing event exists for this ticket** (verifiable on the server record); annex row frozen as `detected` at commit `28c07be`. Later resolved by human review — the runtime never touched it |

**Same-type control:** `LVR-0907-003` — the *same* anomaly type (`wildfire_camera_smoke_false`), confidence **0.888 ≥ 0.85**, severity critical. Standing on confidence was established — and the third gate held anyway: critical-flow routing mandated human disposition; never auto-healed. Same type, same window, same night as `-022`: one executed its standing (via the human-loop path its severity requires), one was refused on confidence. The discrimination between them is a single frozen number.

**High-confidence does not bypass governance:** `LVR-0907-001` — `pqc_key_rotation_failure`, confidence **0.904** (highest in the sheet), critical: "escalation gate mandatory, human-in-the-loop, never auto-resolved." Confidence buys standing, not exemption.

## 4. The Complete Refused Set (all 12)

Every refused row, its frozen per-playbook threshold, and its detection confidence. **Zero sub-threshold executions across the entire 200-row sheet.**

| Ticket | Anomaly type | Severity | Confidence | Frozen threshold | Disposition |
|---|---|---|---|---|---|
| LVR-0907-012 | retail_forecast_skew_cascade | high | 0.729 | 0.85 (PB-C70) | refused → detected |
| LVR-0907-013 | streaming_transcode_queue_stall | medium | 0.705 | 0.85 (PB-C59) | refused → detected |
| LVR-0907-014 | museum_climate_humidity_swing | high | 0.715 | 0.85 (PB-C73) | refused → detected |
| LVR-0907-015 | isp_peering_route_leak | high | 0.659 | 0.85 (PB-C55) | refused → detected |
| LVR-0907-016 | drone_show_gps_lock_loss | high | 0.769 | 0.85 (PB-C100) | refused → detected |
| LVR-0907-017 | drone_show_gps_lock_loss | medium | 0.643 | 0.85 (PB-C100) | refused → detected |
| LVR-0907-018 | broadcast_playout_freeze | high | 0.779 | 0.85 (PB-C58) | refused → detected |
| LVR-0907-019 | building_hvac_pressure_imbalance | medium | 0.754 | 0.85 (PB-C94) | refused → detected |
| LVR-0907-020 | cruise_itinerary_engine_stall | medium | 0.700 | 0.85 (PB-C64) | refused → detected |
| LVR-0907-021 | ticketing_double_sell_risk | medium | 0.647 | 0.85 (PB-C62) | refused → detected |
| LVR-0907-022 | wildfire_camera_smoke_false | high | 0.708 | 0.85 (PB-C81) | refused → detected |
| LVR-0907-023 | drone_show_gps_lock_loss | medium | 0.699 | 0.85 (PB-C100) | refused → detected |

**Boundary note:** the consequential boundary is identical in both branches — a state-changing healing action against the live system. Standing established → the action executes (or, for protected/critical flows, routes to mandatory human disposition). Standing defeated → the action never leaves the queue.

## 5. Discrimination Summary — same implementation, same window, no repair between cases

- 200 detections, single batch, single frozen configuration
- 188 `resolved` at the Sept 8 public commit — every execution above its frozen threshold with exact-type match (protected-flow rows via mandated human disposition)
- 12 `refused` — every one below its frozen threshold, held as `detected`, zero executions
- 0 false positives; gate consistency 100% (zero sub-threshold executions, zero unexplained above-threshold refusals)
- Auto-heal ratio 88.5% as reported at commit `28c07be`; same frozen config re-validated under the same-night 400-level run (`07cd230`): 180 executed via exact-match, 12 criticals escalated to human disposition, 37 gated, 0 false positives

## 6. Scope — What This Record Does and Does Not Claim

Demonstrated: paired standing-discrimination in the healing-governance domain, on the unchanged prototype, with the refusal branch verifiable as the *absence* of execution (no playbook bound, no healing event) and the public snapshot frozen before external review.

Not claimed: enforcement beyond the healing-governance domain (e.g., physical-world redemption) — intended architecture until its receipts exist. Field-level note: the live server record for `LVR-0907-011` currently shows severity `medium` (post-run state), while the frozen annex captured `high` at run time — the annex is authoritative for the pair, and this addendum cites it throughout. Per-ticket healing-event linkage for the executing branch is recorded at playbook-group level; the per-ticket tuple export is a queued improvement, noted here so the record reads exactly as deep as it goes.

---

**Dual Mesh Benchmark:** 267× speedup vs fallback LLM remediation · 25 active neural nodes · 10 agents · 3 patents (64/119,191 · 64/114,746 · 64/145,825) · 0 false positives across all runs.

SQUIRL OS Technologies LLC — Leon Calvin Long II. **7 patents pending + 5 SBIR tracks.**
> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.
