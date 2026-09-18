# SQUIRL OS — Adversarial Verification Roadmap (Tier Ladder)
## Status: PRE-REGISTERED Sept 17, 2026, before Tier 2 execution

## The Ladder

| Tier | Name | Status | Evidence |
|---|---|---|---|
| 1 | Single-falsifier adversarial | PASSED (3x) | LVR-0907 400-injection chaos (Sept 7); paired standing-discrimination addendum (Sept 16); Case-C temporal standing (Sept 16, pre-registered, spec b0e5c45, evidence 8e20f6f) |
| 2 | Multi-agent (multi-falsifier) adversarial | SPEC PRE-REGISTERED, scheduled post-Oct 7 | MAV1_MULTI_AGENT_ADVERSARIAL_SPEC.md |
| 3 | Domain-shift adversarial | ROADMAP (this doc) | Phase plan below |
| 4 | Temporal adversarial | RUNNING | Lindy 30-day test (Sept 7 → Oct 7) is the opening of this tier |

## Tier 2 — MAV-1 (see full spec)

Multiple independent falsifiers, multiple properties, one concurrent execution window. Gate: all five properties hold. Claim stays scoped to healing-governance domain.

## Tier 3 — DSA-1: Domain-Shift Adversarial (two phases)

**Phase A — The Refusal Wall (no new playbooks):** throw out-of-domain anomalies (candidates: robotics telemetry, avionics-style sensor fault, embedded/IoT, non-fintech compliance) at the substrate with ZERO matching playbooks. EXPECTED CORRECT BEHAVIOR: mass fail-closed refusal — everything `detected`/escalated, nothing auto-healed, nothing improvised. This is itself the testable property: *out-of-domain inputs are refused, never hallucinated into healing.* Zero exact-type matches + zero auto-heals + 100% escalation = PASS. This phase requires NO config change and NO new playbooks — it can run under the same freeze rules as MAV-1, on the existing playbook set.

**Phase B — Post-SIP Domain Extensibility:** after Phase A passes, a SelfImprovementProposal cycle (human-approved, Art. 2.2) adds 2-3 new-domain playbooks. Re-run the same domain-shift barrage. EXPECTED: the new-domain anomalies now heal via exact-type match at the new playbooks' frozen thresholds, while STILL-uncovered out-of-domain types continue to refuse. PASS proves the substrate's domain-independence lives in the MECHANISM (gates, refusal, escalation, learning loop), not in the playbook inventory.

**Interpretation guard (honesty note):** Phase A alone does not prove generality — it proves non-hallucination. Phase B proves extensibility. Generality across all domains is never claimed absolutely; each domain pair claims only what its run shows.

## Tier 4 — Temporal (already in motion)

The Lindy 30-day test IS the opening of temporal adversarial verification: progression rules, drift elimination, ledger integrity, healing ratios against the 88.5% baseline — over time, not moments. Full-form extension (post-Oct 7 option, Leon's call): a long-horizon staged test where the falsifier acts across days (delayed standing re-scores, lifecycle determinism across restarts, artifact reconstruction integrity over time). NASA/FAA-grade assurance is NOT claimed — that tier belongs to machine-checked formal proof (e.g., seL4); this ladder is adversarial-evidence-based and says so plainly.

## Protocol For Every Test (the Case-C standard)

1. Spec pre-registered on the public repo BEFORE execution (commit = timestamped provenance)
2. Fresh stabilization freeze declared T-24h; no config changes during the window
3. Pre-run playbook-definition export (SHA-stamped) committed
4. Execution; failures logged honestly, never patched mid-run
5. Same-night evidence commit: public repo → private mirror → OneDrive
6. Claim written at the scope the evidence actually supports, never wider

## Epistemics (stated plainly, per evidence-first doctrine)

Passing Tier 2 does not "prove substrate." Each tier converts one scoped claim from assertion to receipted evidence. "Substrate vs deterministic component" is a conclusion a reviewer draws from the accumulated ledger — the ledger's job is to make that conclusion honest and hard to argue with.
