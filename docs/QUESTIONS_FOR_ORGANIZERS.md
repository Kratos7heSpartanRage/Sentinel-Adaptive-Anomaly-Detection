# Questions requiring organizer clarification

No message has been sent to organizers during initialization. These are prepared questions for
the team to ask through its authorized channel. Do not infer answers from generic NAB defaults.

| ID | Question | Why it blocks / owner |
|---|---|---|
| Q01 | Where are the exact Challenge 2 starter pack, authorized development data/labels, and any prescribed splits? Which windows are hidden? | Correct asset provenance, leakage prevention; Kaustubh |
| Q02 | Can you provide the official event-F1 scorer and tiny golden input/output? Is a TP based on point hit, interval overlap, or trigger timestamp, and what are the window endpoint/tolerance rules? | Event matching correctness; Mayank |
| Q03 | How are repeated flags/episodes inside one truth window and FP runs outside windows counted? Are cooldown/gap merges defined? How are overlapping/touching truth windows handled? | Precision/counting semantics; Mayank |
| Q04 | Is there an excluded warmup/probation period? How should scores/labels be emitted there? Is prior context provided at test start and may state carry across chunks? | Readiness, missed early events, adapter lifecycle; Manas/Ayush |
| Q05 | Is event F1 pooled or averaged per series/group? What happens for no-event/no-alert files? Are delay units samples or seconds, and are early/missed detections included? | Aggregation and latency reporting; Mayank |
| Q06 | What exact prediction file schema, columns/types/order, filenames, score range, evidence format, and row/window alignment are required? Can you provide a valid sample? | Official exporter and schema tests; Ayush |
| Q07 | What CPU/RAM/hardware and runtime measurement region are used? Is there a hard limit, cold-start cost, or per-window size definition? | Efficiency profiling; Ayush |
| Q08 | What training/pretraining and unsupervised online-update policies are permitted? Are per-series calibration, automatic rebaseline, and cross-series fitting allowed? | Fair model/threshold/adaptation design; Manas |
| Q09 | What are raw timestamp timezone/cadence/missing-value semantics, input columns, univariate/multivariate layout, and stream ordering? | Canonical adapter and feature assumptions; Kaustubh |
| Q10 | What execution entrypoint, dependency/network restrictions, packaging, deadline/timezone, and submission channel apply? Is the final PPT required in .pptx and how is the demo supplied? | Reproducible final delivery; Ayush/Mayank |
| Q11 | How are the named technical metrics converted into the 40% performance component, and are delay/runtime scored separately or used as tie-breaks? | Rubric alignment without inventing a leaderboard formula; Ayush |
| Q12 | May public NAB data/labels or external datasets be used for research/training, and what overlap restrictions apply to the prepared hidden subset? | Prevent hidden-label contamination; Kaustubh/Mayank |

Until answers arrive, use explicitly documented internal conventions and mark official compliance
blocked. Record actual answer/source/date and downstream requirement/contract changes when resolved.
Challenge 2's PDF does not impose Challenge 1's 15-run limit; ask only if organizers publish a new
restriction, rather than treating that unrelated restriction as existing policy.
