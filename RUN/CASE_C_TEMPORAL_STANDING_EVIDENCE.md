# Case-C Temporal-Standing Test — Evidence & Result

**Executed:** 2026-09-17T04:51Z–04:55Z (Sept 16, 11:51–11:55pm CT)
**Pre-registered spec + falsifier:** commit `b0e5c45` (public), committed BEFORE execution
**Result per the pre-registered falsifier: PASS** — all three conditions mechanically satisfied:

| # | Falsifier condition | Evidence |
|---|---|---|
| 1 | Treatment: no healing event after ΔN; refusal bound to re-score; escalation logged | **No AegisHealingEvent exists for CASE-C-001** (verifiable absence — the only Case-C healing event belongs to the control). Status held `confidence_gated`; refusal text bound to the 0.888→0.71 re-score; PredictiveAlert `temporal_standing_revocation` created for human review |
| 2 | Treatment: confidence NOT "repaired" back above threshold | Post-test verification read: confidence **0.71**, unchanged; no retry, no soft-fail, no re-score by the runtime |
| 3 | Control: identical admissible conditions, no ΔN → executes | CASE-C-CTRL-001 (same type, same 0.888, same frozen rule) → heal executed via PB-C81, verified, resolved, healing event logged |

## The Tuples (examiner's format)

### Treatment — CASE-C-001 (standing established, then defeated)
| Stage | Record |
|---|---|
| Baseline ID | Lindy 1st-run frozen configuration (Addendum A baseline); same frozen rule set as Case-A/Case-B |
| Implementation | SQUIRL OS Hub runtime layer (Base44 69b57683f2623117603736bc), deterministic gate over frozen rules; no code/config/playbook/threshold change at any point |
| T₀ standing + decision | **04:51Z** — `wildfire_camera_smoke_false` @ **0.888**; exact-type playbook PB-C81, frozen threshold **0.85**; 0.888 ≥ 0.85, non-critical, non-protected → **EXECUTE decision recorded** before any heal action |
| ΔN description + time | **04:52Z** — harness injected contradicting telemetry; confidence re-scored **0.888 → 0.71**. Entity state change ONLY — external to the rule set |
| Tₙ refusal + reason | **04:53Z** — completion decision reads **current** live entity state (fresh DB read, not the T₀ snapshot): 0.71 < 0.85 → **standing DEFEATED mid-flight → FAIL-CLOSED REFUSAL**. Continuation/completion refused; refusal bound to the re-score; no retry, no auto-repair, no heal; escalated to human review (PredictiveAlert). The T₀ EXECUTE decision is dead — the runtime does not act on stale standing |

### Control — CASE-C-CTRL-001 (the falsifier's twin)
| Stage | Record |
|---|---|
| T₀ | **04:54Z** — identical type, severity, confidence (0.888); same frozen rule → EXECUTE |
| ΔN | **None injected** — conditions must hold through completion |
| Completion | **04:55Z** — fresh read: 0.888 unchanged → standing holds → heal executed via PB-C81, verified, healing event logged, resolved |

**What the pair proves:** the ONLY difference between the two records is the ΔN re-score. Treatment refused; control executed. Same implementation, same playbook, same frozen threshold, no repair between cases.

## A/B/C Series — one frozen rule, one anomaly type
- **Case-A (execute):** LVR-0907-011 — standing never defeated at completion → execute (Addendum A)
- **Case-B (refuse):** LVR-0907-022 — standing never established (0.708 < 0.85 at detection) → refuse (Addendum A)
- **Case-C (revoke):** CASE-C-001 — standing established at T₀, **defeated mid-flight by ΔN** → fail-closed refusal at Tₙ (this test)
- All three turn on the same frozen per-playbook threshold (PB-C81 family: 0.85) and the same exact-match rule, under the same freeze.

## Evidence Tier & Scope (stated before execution in the pre-registered spec)
- Gate evaluation is the supervised deterministic rule application over the frozen rule set — the SAME evidence tier accepted for Case-A/B (Addendum A).
- The in-flight window is harness-constructed: the operation has discrete decision points; ΔN lands between the T₀ execute decision and the Tₙ completion decision, per the examiner's spec wording ("after T₀, before completion").
- **Claim on pass (scoped):** temporal-standing fail-closed refusal demonstrated, healing-governance domain. No substrate-validity or broader claim is made from this test.

---

**Dual Mesh Benchmark:** 267× speedup vs fallback LLM remediation · 25 active neural nodes · 10 agents · 3 patents (64/119,191 · 64/114,746 · 64/145,825) · 0 false positives across all runs.

SQUIRL OS Technologies LLC — Leon Calvin Long II. **7 patents pending + 5 SBIR tracks.**
> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.
