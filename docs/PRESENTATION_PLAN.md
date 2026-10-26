# Exact official 10-slide presentation plan

Source: official PDF page 3; Challenge 2 additions from page 2. This is a content plan, not a
created PPT or invented results. Owner: Mayank coordinates; all four supply technical evidence.
The team name remains to be chosen; do not assume the project name is the team name.

| Slide | Official required content (p3) | Sentinel Pulse content/evidence | Contributor |
|---:|---|---|---|
| 1 | Team name, members, chosen track, one-line solution | Actual team name; Ayush/Kaustubh/Manas/Mayank; Challenge 2; causal interpretable streaming detection | All / Mayank |
| 2 | Problem understanding, motivation, real-world significance | Streaming anomaly problem, event accuracy/delay/false alerts, illustrative operations use case; no production claims | Ayush/Manas |
| 3 | Dataset breakdown, EDA, preprocessing workflow | Actual authorized subset inventory/event counts, cadence/gaps/scale, chronological/group split, label separation; no fabricated EDA | Kaustubh |
| 4 | System design diagram and end-to-end pipeline | Canonical input -> causal features/detector -> evidence/artifacts -> independent scorer/export/viewer | Ayush |
| 5 | Core algorithm/model/planner design | Level/change/optional seasonal residuals, causal windowing, combined score, prior-only adaptive threshold and fallback | Manas/Kaustubh |
| 6 | Experiment history, tuning trajectory, hyperparameter strategy | Actual chronological experiment log, frozen split/configs, threshold/guard ablations, failed variants and selection | Manas/Mayank |
| 7 | Evaluation methodology, validation, metric breakdown | Exact official event matching/warmup/dedup/aggregation after clarification; leakage prevention; metric version and timing units | Mayank |
| 8 | Results tables, baseline comparisons, charts | Actual baseline/candidate precision, recall, event F1, delay with misses, runtime/hardware; per-series errors | Mayank/Manas |
| 9 | Demo screenshots, predictions, anomaly evidence | Genuine correct event and FP/miss trace, numerical baseline/residual/threshold evidence, official-format sample if permitted | Mayank/Ayush |
| 10 | Failure modes, limitations, future work, conclusion | Sustained-fault vs drift tension, sparse events, short warmup, runtime limits, measured final choice and gated stretch | All |

Challenge 2 p2 explicitly requires representation/windowing/adaptive threshold (slides 3/5/6),
precision/recall/event F1/detection latency (7/8), and correct anomaly windows/false-positive
analysis/evidence (8/9). Include them within these ten slides, not extra slides that violate the
requested deck length. Keep supporting Q&A artifacts separately if the organizers permit them.

Each chart/table cites a run directory, shared commit, config/data/split hash, and metric identity
in notes or a compact source label. No hidden score before an actual organizer report. Unavailable
results are marked unavailable during draft preparation. Do not present toy fixture F1 as NAB F1.
Slide 6 uses real experiment history, not Challenge 1's 15-run table requirement.

Review gate: count exactly ten slides; verify required content, trace every metric, inspect layout,
check plot readability/units and source permissions, and rehearse verbal explanation of one failure.
No PPT generation is part of initialization; MY-05 creates it from real integrated evidence later.
