# Official problem analysis

Source: `Utkrishta 2026 Participant Problem Statements.pdf`, all three pages read.
SHA256: `b93d18863425418a296cdbfe14335de73a69761f69d537d88fddb72b917f3ef0`.
The original PDF remains unchanged at the repository root. See [traceability](REQUIREMENTS_TRACEABILITY.md).

## VERIFIED_OFFICIAL_REQUIREMENT

Page 2 selects **Challenge 2 - Sentinel**, theme **Adaptive Time-Series Anomaly Detection**.
Build a lightweight system that learns baseline behavior from streaming time-series data,
identifies observations/windows that deviate, and provides anomaly scores, binary
NORMAL/ANOMALOUS labels, and interpretable evidence for every flagged event.

The dataset is a NAB subset prepared in the starter pack, with hidden test windows. Event-based
F1 is primary. Precision/recall assess flagged windows against true events. Detection delay
measures onset-to-trigger latency; inference runtime measures speed per streaming window.
No aggregation formula, hard runtime ceiling, CPU/RAM budget, or numeric target is provided.

Permitted examples: rolling z-score, Isolation Forest, LOF, One-Class SVM; autoencoders,
temporal clustering, sliding adaptive thresholds, hybrid ensembles. This is permission to
consider techniques, not a requirement to use every family.

Page 3 requires runnable source/notebooks, local setup/reproducibility README, predictions in
the organizer schema, an exact 10-slide PPT, and a brief live/video demo. Challenge 2's slide
content also includes representation/windowing/threshold logic; precision/recall/event F1/delay;
correct anomaly windows, false positives, and evidence examples.

Judging weights: technical performance 40%, approach/innovation 20%, efficiency/constraints 15%,
presentation 15%, code/demo 10%. Technical performance uses hidden evaluation. Challenge 2
efficiency concerns runtime. The **15-training-experiment restriction is explicitly Challenge 1**
(page 1); do not transfer its efficiency multiplier or ROC-AUC objective to Challenge 2.

## ENGINEERING_ASSUMPTION

Start with independent univariate series because NAB is the named corpus; confirm the prepared
subset's actual columns. Treat observations as ordered, replayable streams, with finite numeric
values and explicitly normalized UTC timestamps. Warmup is internal NORMAL/score-null, never
evidence of a genuinely normal point. No assumption that hidden data is accessible or benign.
Use CPU local execution and bounded state; these are feasibility choices, not organizer limits.

## DESIGN_DECISION

Choose Sentinel Pulse: a causal residual detector with robust level/change features, optional
past-only seasonal prediction, empirical score thresholds, and experimentally gated adaptation.
Start with a rolling MAD baseline. Keep inference, evaluation, and visualization separate.
Internal JSONL is not an organizer submission schema. Official adapters remain explicit tasks.

## REQUIRES_ORGANIZER_CLARIFICATION

Missing: starter pack, development labels, official scorer, output columns/types, timezone,
warmup scoring, event matching/deduplication, window boundaries, overlap policy, averaging across
series, training restrictions, allowed online updates, hardware/runtime protocol, submission
entrypoint/dependencies, and deadline. See [questions](QUESTIONS_FOR_ORGANIZERS.md).

## Why the problem is difficult

- Spikes, variance bursts, level shifts, and missing seasonal peaks require different context.
- Fast adaptation can learn an actual fault as the new normal; slow adaptation yields alert storms.
- A long contextual window delays onset detection, while a short one follows noise.
- Whole-series normalization, centered smoothing, random overlapping-window splits, and revised
  historical scores leak future information or labels.
- Event-level scoring can reward very different behavior from point F1. Alert grouping and
  warmup exclusions can change scores substantially and must match organizer semantics.
- Explanations should expose the actual pre-update baseline and threshold; causal root cause
  cannot be inferred from one univariate signal alone.

The strongest feasible design is therefore conditional on validation, not an asserted benchmark
winner. Dataset-specific claims and all performance results remain unavailable at initialization.
