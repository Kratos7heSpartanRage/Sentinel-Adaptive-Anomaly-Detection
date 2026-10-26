# Requirements traceability

All OFF rows are **VERIFIED_OFFICIAL_REQUIREMENT** from the original PDF at repository root.
Page numbers are one-based. Planned verification is not a claim that the requirement is met.
INIT-01 creates the foundation; personal task IDs point to remaining work.

| ID | Page | Requirement | Planned implementation / task | Verification | Owner / state |
|---|---:|---|---|---|---|
| OFF-01 | 2 | Lightweight streaming baseline learning | Per-series sequential detector; AY-03, MN-01/02 | Prefix invariance, bounded-state profiling | Ayush / starter only |
| OFF-02 | 2 | Detect anomalous observations or windows | Residual scoring and alerts; MN-02/03 | Held-out event performance | Manas / starter only |
| OFF-03 | 2 | Anomaly score for each flag | Nonnegative internal scores; MN-02 | Schema/finite-score tests and export mapping | Manas / internal only |
| OFF-04 | 2 | NORMAL/ANOMALOUS binary label | Threshold decision; MN-03, AY-04 | Boundary tests and official schema roundtrip | Manas, Ayush / internal only |
| OFF-05 | 2 | Interpretable evidence for every flag | Pre-update baseline, scale, residual, components; MN-02, MY-03 | Explanation arithmetic/visual inspection | Manas / minimal evidence exists |
| OFF-06 | 2 | Organizer-prepared NAB subset, hidden windows | Provenance/asset adapter; KS-01/04 | Manifest hashes, organizer source confirmation | Kaustubh / assets missing |
| OFF-07 | 2 | Primary event-based F1 | Official scorer integration; MY-04 | Golden cases against organizer implementation | Mayank / blocked |
| OFF-08 | 2 | Precision and recall | Matched-event counts; MY-01/04 | Hand-derived cases, official parity | Mayank / provisional only |
| OFF-09 | 2 | Onset-to-trigger detection delay | Timestamp matching; MY-01/04 | Known delayed-trigger cases | Mayank / provisional only |
| OFF-10 | 2 | Inference runtime per streaming window | Timing distributions; AY-01/06 | Hardware-tagged repeated measurements | Ayush / per-point timing only |
| OFF-11 | 2 | Permitted statistical/ML/advanced approaches | MAD baseline, residual hybrid; MN-01/02/03 | Method explanation and scope review | Manas / plan conforms |
| OFF-12 | 2 | PPT: representation, windowing, adaptive threshold | Slides 3/5/6; KS-02, MN-03, MY-05 | Inspect real implementation and exact deck | Kaustubh, Manas / planned |
| OFF-13 | 2 | PPT: precision, recall, event F1, latency | Slides 7/8; MY-04/05 | Trace figures to immutable run manifests | Mayank / blocked on results |
| OFF-14 | 2 | PPT: true events, false positives, evidence | Slides 8/9; MY-03/05 | Genuine outputs and error examples | Mayank / planned |
| OFF-15 | 3 | Fully functional source/notebooks and local instructions | Python package and runnable CLI; AY-05 | Clean-clone setup and core tests | Ayush / starter only |
| OFF-16 | 3 | README: setup, environment, experiments, reproduction | README and experiment docs; AY-05 | Follow commands on clean environment | Ayush / starter documented |
| OFF-17 | 3 | Standardized prediction file in organizer schema | Explicit exporter; AY-04 | Validate provided schema and golden file | Ayush / schema missing |
| OFF-18 | 3 | Final PPT has exactly 10 required slides | PRESENTATION_PLAN; MY-05, all supply content | Slide count/content checklist | Mayank / plan only |
| OFF-19 | 3 | Brief working live/video demonstration | CLI plus optional artifact viewer; MY-03/05 | Offline rehearsal, saved fallback | Mayank / CLI foundation only |
| OFF-20 | 3 | 40% technical performance on hidden data | Selection by validated event F1; MY-02/04 | Organizer result only establishes hidden score | Mayank / not evaluated |
| OFF-21 | 3 | 20% approach/innovation | Guarded residual/threshold ablations; MN-04/05 | Compare components, defend contribution | Manas / hypothesis |
| OFF-22 | 3 | 15% efficiency/constraints; Ch2 runtime | CPU inference and profiling; AY-06 | Organizer runtime protocol when received | Ayush / protocol missing |
| OFF-23 | 3 | 15% presentation quality | Exact deck and Q&A; MY-05 | Team rehearsal and checklist | Mayank / planned |
| OFF-24 | 3 | 10% code/demo quality | Contracts, tests, docs, optional viewer; AY-05/MY-03 | Reproduction and demo failure rehearsal | Ayush, Mayank / foundation |

## Other classification records

| ID | Classification | Statement | Resolution/owner |
|---|---|---|---|
| ASM-01 | ENGINEERING_ASSUMPTION | Univariate numeric series initially | Inspect starter columns; KS-01/04 |
| ASM-02 | ENGINEERING_ASSUMPTION | CPU local execution feasible | Confirm hardware; AY-06 |
| ASM-03 | ENGINEERING_ASSUMPTION | Explicit-offset timestamps internally | Confirm raw timezone; KS-04 |
| DD-01 | DESIGN_DECISION | UI-independent core, JSON/JSONL internal artifacts | ADR-01/02; Ayush |
| DD-02 | DESIGN_DECISION | Rolling MAD starter, guarded residual system planned | ADR-03; Manas |
| DD-03 | DESIGN_DECISION | No future-aware transforms or label-fed inference | ADR-04; all |
| Q-01 | REQUIRES_ORGANIZER_CLARIFICATION | Event matching/averaging/warmup | Questions Q02-Q05; Mayank |
| Q-02 | REQUIRES_ORGANIZER_CLARIFICATION | Official submission schema | Question Q06; Ayush |
| Q-03 | REQUIRES_ORGANIZER_CLARIFICATION | Runtime and execution environment | Questions Q07/Q10; Ayush |
| Q-04 | REQUIRES_ORGANIZER_CLARIFICATION | Dataset access, update permissions | Questions Q01/Q08/Q09; Kaustubh |

Slide-by-slide page-3 requirements are mapped in [PRESENTATION_PLAN](PRESENTATION_PLAN.md).
Challenge 1's training budget, ROC-AUC/PR-AUC, and multiplier have no Challenge 2 traceability row
because the official document scopes them to Challenge 1.
