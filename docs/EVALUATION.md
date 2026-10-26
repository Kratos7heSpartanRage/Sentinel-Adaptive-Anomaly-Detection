# Evaluation semantics and honest reporting

The official PDF (p2) makes **event-based F1** primary and names precision, recall, detection
delay, and inference runtime. It does not define the event matching algorithm, averaging,
warmup exclusion, false-positive grouping, overlap handling, or exact execution protocol.
The organizer's scorer must resolve those questions. NAB's normalized score is a different
metric and must never be labeled the hackathon score.

## Four evidence levels

| Scope | Data/scorer | Allowed claim |
|---|---|---|
| Synthetic smoke | Explicit artificial wiring fixtures; provisional evaluator | Code path and arithmetic work on an example only |
| Development validation | Permitted labeled development assets and frozen splits | Named local metric on that exact split; state scorer version |
| Official benchmark evaluation | Organizer-authorized data, official scorer and schema | Official-metric local benchmark result for that exact dataset/split only |
| Organizer-held hidden evaluation | Organizer runs frozen submission against hidden windows | Only an actual organizer-reported score is a hidden result |

Starter CLI supports only the first two scopes. `development_validation` is a declaration by
the operator; it does not validate dataset authorization or convert the provisional metric into
the official one. Neither official benchmark nor hidden evaluation has been performed.

## Provisional reference policy v0 (implemented)

Identifier `provisional_event_trigger_f1_v0`, `official_metric=false`. This makes software
integration testable before the official scorer exists. It is **not an inferred official rule**.

1. Truth windows are closed [start,end], disjoint and non-touching within a series. Overlap is
   rejected rather than silently merged. Windows must fit the recorded per-series timestamp span.
2. Each maximal run of consecutive ANOMALOUS rows within a series is one predicted episode.
   Interleaving other series does not interrupt a run. No wall-clock gap merge or cooldown is used.
   Only the episode's first timestamp is a trigger. NORMAL ends an episode.
3. A trigger inside an unmatched truth window matches that event once. An unmatched trigger is
   FP, including a second episode inside an already-matched truth window. Unmatched truth is FN.
4. An episode starting before a window and continuing into it is **not** credited as a hit. This
   conservative trigger policy is deliberately explicit and may differ from organizer overlap rules.
5. TP = matched windows; precision=TP/(TP+FP), recall=TP/(TP+FN), F1=2TP/(2TP+FP+FN).
   A zero denominator yields 0.0 by convention, including no events/no alerts. Report counts so
   empty-series behavior is not hidden. Empty prediction files are rejected.
6. Delay is trigger time minus matched-window start, in seconds, for hits only. No hits -> null mean.
   Always report FN alongside delay; mean delay alone hides missed events. Early credit is absent.
7. Warmup points are included in coverage and emit no alert; events during warmup may be missed.
   The evaluator does not silently drop them. This is an internal policy pending organizer guidance.
8. Validate schema, score/readiness/label agreement, monotonic per-series predictions, and manifest
   prediction checksum. Do not read labels during inference or alter predictions during scoring.

The reference evaluator checks broad timestamp coverage, not continuous sampling within every
truth window; gap diagnostics belong in the dataset audit. It scans each series' truth windows
per trigger and is intended for correctness/fixtures rather than a claimed optimal scorer.
Boundary/deduplication/empty/warmup/overlap/coverage cases need golden fixtures (MY-01).

## Official metric integration gate

Mayank obtains the actual scorer/version and documents matching, tolerance, windows, probation,
duplicates, no-event behavior, averaging, and output ordering. Build tiny hand-labeled examples,
then compare counts and F1 against the official implementation. Confirm with organizers if
examples conflict with prose. Ayush maps internal output via the approved exporter. Keep the
provisional metric available under its old identifier; do not silently change its semantics.

Official aggregation takes priority. Additional pooled micro event F1 and per-series macro F1
are diagnostics, with no-event handling stated. A macro average is not interchangeable with a
pooled count calculation. Detection delay should include median/p95 for hits plus missed-event
count; specify sample versus elapsed-time units. Record the timing boundaries for inference.

## Selection and final reporting

Tune on training/validation only. Freeze split manifests and candidate ordering before comparing.
Use untouched series/groups for final local evaluation if data permits. Thresholds may use only
past residuals at inference and never hidden labels. Ban whole-series scaling, centered filters,
test-label threshold sweeps, point-adjusted F1, and revising previously emitted scores.

Each result record must identify data provenance, series/event counts, split hashes, metric and
scorer version, model/config, code revision/dirty state, seed if stochastic, environment/hardware,
precision/recall/F1/counts, delays, timing, and failure analysis. Current starter manifests cover
only a subset; AY-01 and MY-02 own completion. No dataset inventory or official F1 is available yet.

For final evaluation: verify permission/assets -> reproduce baseline -> freeze config/code ->
run the untouched split once -> validate official-format output -> archive hashes/report ->
submit according to organizer instructions. Hidden evaluation labels remain inaccessible; do not
seek public-label shortcuts for suspected hidden series.
