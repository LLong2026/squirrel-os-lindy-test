# 🐿️ SQUIRL OS — The 30-Day Lindy Test (First Run)

**Live, dated, unedited. September 7 → October 7, 2026.**

The Lindy Test is a simple bet: we point SQUIRL OS — a self-healing AI infrastructure — at its own operation, freeze the configuration, and let it run for **30 consecutive days.** Heartbeat monitoring, anomaly detection, playbook-driven healing, pattern learning — all of it, on its own. No hotfixes mid-run. Whatever doesn't survive gets fixed *after* the run, and the failure itself becomes learning material.

The run window's public record lives in the [`RUN/`](RUN/) folder and updates as the test progresses:

- **[`RUN/DAILY_LEDGER.md`](RUN/DAILY_LEDGER.md)** — one honest entry per day: uptime verdict, checkpoints, incidents (self-healed incidents are logged as **wins**)
- **[`RUN/LEARNING_LOG.md`](RUN/LEARNING_LOG.md)** — every pattern and defect the run surfaces, written down
- **[`RUN/SQUIRL_OS_INCIDENT_LEDGER.xlsx`](RUN/SQUIRL_OS_INCIDENT_LEDGER.xlsx)** — the full dated incident record, row by row
- **[`RUN/BENCHMARK_LINDY_30_FINAL.md`](RUN/BENCHMARK_LINDY_30_FINAL.md)** — the formal benchmark, written at run close

Every update is a dated git commit. The ledger keeps itself.

## Why "Lindy"?

If a system survives, it was probably built right. 30 days of continuous, self-supervised operation is the credibility benchmark that matters — not a demo, not a benchmark score. A ledger that shows what actually happened, including what went wrong and how it healed, is worth more than any polished pitch.

## The Cage Thesis

> **"The irony is beautiful — the tools everyone trusts blindly become the proof that nothing should be trusted blindly."**

*Design principle for the post-Lindy LLM-cage program, October 2026.*

Third-party LLMs — Copilot, Grok, all of them — drift and fabricate on the regular. SQUIRL OS's answer is not a better model. It's a deterministic cage: every output, ours or anyone's, validated against invariant contracts before anyone sees it. The same governance layer that held this runtime frozen for 30 unedited days is what makes it safe to run *any* LLM inside the boundary. Caged third-party models are queued for the post-Lindy program — and every hallucination they throw at the gate is free adversarial test data for the validation layer.

## Dual Mesh Benchmark

- **267× speedup** (800ms → 3ms anomaly lookup)
- **25 active nodes** (5 read + 13 interconnect + 7 write)
- **10 agents** communicating collision-free
- **3 patents covering** (64/119,191 · 64/114,746 · 64/145,825)
- **0 false positives** across 70+ stress test anomalies

## Sponsors & Support

If this run is worth something to you, this repo carries a **FUNDING.yml** — GitHub will show you a "Sponsor" button right on this page. Every record here is timestamped and cross-checkable.

- **Company:** [squirlos-technologies.com](https://squirlos-technologies.com)
- **Contact:** support@squirlos-technologies.com — same-business-day response, 24/7 system monitoring behind it
- **Research archive:** [doi.org/10.5281/zenodo.21613628](https://doi.org/10.5281/zenodo.21613628) (64 records)
- **Master DOI roadmap:** [MASTER_DOI_ROADMAP.md](MASTER_DOI_ROADMAP.md) — every live DOI and exactly which site each record lives on (Zenodo / OSF / EngrXiv / GitHub)
- **Master research index:** [RESEARCH_LINKS.md](RESEARCH_LINKS.md) — author identity (ORCID), every canonical DOI, and all distribution surfaces (Zenodo, EngrXiv, GitHub, X) on one page
- **GitHub:** [github.com/LLong2026](https://github.com/LLong2026) · **X:** [@leonlongITC1](https://x.com/leonlongITC1)

**7 patents pending + 5 SBIR tracks.**

---

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

© 2026 Leon Calvin Long II / SQUIRL OS Technologies. All rights reserved.
