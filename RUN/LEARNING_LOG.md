# LINDY 30 — Learning Log (1st Run)

Every pattern, defect, and observation the run surfaces. The self-learning loop, written down. Honest entries only — wins AND cracks.

---

## L1 — Enforcement material matters (Day 1, Sept 7)
**Observation:** Jasper's constitution hardcodes owner timezone (America/Chicago) as PROSE. A platform UTC timestamp outvoted it in the persona layer; the human caught the drift. Meanwhile, the same constitution's ENFORCED articles (gates, cages, money-blocks) held all day under a 200-anomaly gauntlet — including a 4x refusal of the guardian agent's own deployment attempt.
**Lesson:** Advisory (prose) constitution articles can be outvoted by louder runtime context. Controls (gates, cages) cannot be outvoted — they refuse. Anything that must NEVER drift (identity, timezone, ownership) should eventually live as a runtime control, not a paragraph.
**Status during run:** No fix — freeze holds. Logged as a spec-cabinet candidate for post-run.

## L2 — aegisAnomalySync recovery (Day 1, Sept 7, 7pm CT)
**Observation:** The Hypervisor aegisAnomalySync function — a silent no-op across 3 prior builder passes — executed correctly during the 7pm reconciliation (6 records synced, 0 errors). First documented success since the freeze began.
**Hypotheses:** (a) the builder pass that created test record LVR-0907-TEST-1 also fixed the function in-editor, or (b) the function only works under certain session contexts and the 7pm workflow context was valid. Needs 2+ more successful runs to confirm a pattern.
**Status during run:** Watching. If it holds across the next reconciliation cycles, the Hypervisor mirror may be self-healing back to trustworthy — which would itself be a Lindy win.

## L3 — Cage integrity: owner intent does not equal owner click (Day 1, Sept 7)
**Observation:** With the owner's explicit spoken approval ("I approve the canary change, go ahead and make it"), the guardian agent was still refused by the Arete deploy cage 4x. No agent-callable approve path exists on the deployment function.
**Lesson:** The human-approval gate binds the APPROVAL ACT to the owner's own hand in the UI — relaying approval through an agent cannot substitute for it. This is the Art. 2.2 human-in-the-loop control working at full strength, and it's a marketable proof point.

## 4. The 600-Second Ceiling (Day 1, 11pm catastrophe run)

**Observed:** The Monday Catastrophe Stress Test at the 400-injection level exceeded Base44's hard 600-second agent conversation cap — the run died mid-injection (193/400) with zero heals executed. The 200-level runs fit comfortably; 400 does not. This is a platform constraint, not a system defect: the healing loop, gates, and escalation chain all executed perfectly once given room to run.

**Lesson:** The chaos ramp's ladder assumption (200→400→600→800→1000 in a single workflow conversation) hits a wall at 400. Every level above 200 needs a different execution shape.

**Fix when freeze lifts (SIP candidate):** Split the run into two workflow steps — injection step (bounded, fits in window) and heal step (its own conversation window, triggered after injection completes). This also makes the runs more observable: injection stats land even if healing is slow. Not applied mid-run — the Lindy test watches the configuration as-is, and the failure is the data.
