# Shared contracts v1.0

Custodian: Ayush. Typed definitions: `src/sentinel/contracts.py`. This document distinguishes
implemented formats from planned extensions; no external endpoint is part of the current design.

## Canonical input (implemented)

CSV header must be exactly `series_id,timestamp,value` in that order. `series_id` is a nonempty
string; `timestamp` is ISO 8601 with an explicit offset, normalized to UTC; `value` is finite float.
Offsets represent instants, not local clock order. Timestamps strictly increase **within each
series**, including interleaved input. Duplicate times/NaN/Inf/missing fields/extra label columns
are rejected. No implicit sorting, resampling, or imputation. Empty input is an error.

`Observation(series_id: str, timestamp: datetime, value: float)` has no label field. One observation
is currently one point-sized streaming window; future trailing windows end at the current timestamp.
Raw NAB `timestamp,value` input needs KS-04 to supply the series ID and approved timezone. Do not
rename/assume a raw timestamp convention silently. Series cardinality is bounded by max_series.

## Feature boundary (typed now; extractor not implemented)

`FeatureExtractor.process(Observation) -> FeatureFrame` and `reset() -> None` operate per series.
The frame fields are `series_id`, `timestamp`, `expected_level`, `expected_delta`, `scale`, `delta`,
`seasonal_expected`, `history_size`, `ready`. Expected values and scale use strictly earlier
observations; delta may use current value minus the preceding value. `scale` is positive when
ready; expected_level/expected_delta/scale may be null in warmup; seasonal_expected is null until
a validated period has sufficient past context. All present numerical values must be finite.
KS-02 implements this contract; MN-02 can use a deterministic fake FeatureExtractor meanwhile.
RollingMADStarter does not use FeatureFrame and remains runnable if feature development stalls.

## Detector boundary and lifecycle (implemented)

`Detector.process(Observation) -> Prediction` and `reset() -> None`. A detector instance handles
exactly one series, rejects non-increasing times, builds its decision from pre-update state, and
then updates. The owner of a wrapping detector calls its extractor once per point. Calling process
twice for the same timestamp is an error, not an idempotent retry. Reset clears all state. The
pipeline constructs one detector per series with a factory. No training labels or evaluation
objects may be passed to a detector.

`Prediction`: series_id, UTC timestamp, original value, score (float|null), threshold (positive
float), label (`NORMAL`|`ANOMALOUS`), ready (bool), evidence (Evidence). A ready score is finite,
nonnegative, and **not a probability**. Label is ANOMALOUS iff ready and score >= threshold.
Warmup uses score=null, ready=false, NORMAL; official acceptance of warmup mapping is unresolved.

`Evidence`: baseline/scale/residual (float|null), history_size (int), reason (algorithmic string),
component_scores (map of named finite nonnegative magnitudes). Starter reason is `warmup` or
`rolling_mad_deviation`, with component `level`. Evidence is captured before updating; residual
equals value-baseline when ready, scale=max(1.4826*MAD, scale_floor), score=abs(residual)/scale.
Future components `change` and `seasonal` require documented comparable normalization and
combined-score calibration. Evidence describes statistical deviation, not physical cause.

## Prediction serialization and run artifacts (implemented)

`predictions.jsonl`: one JSON object per input row, original order. Fields are Prediction fields
plus `schema_version="1.0"` and `elapsed_ns` (integer >=0). Evidence is a nested JSON object.
UTC timestamps end in Z. Artifact text uses LF newlines across platforms so shared checksums remain
stable under Git's newline policy. All JSON output disallows NaN/Inf. Unknown future fields may be ignored
by compatible readers; required fields/semantics cannot change without the protocol below.

`run.json` includes schema/package version, algorithm, evaluation_scope, dataset_id, input and
prediction SHA256, resolved configuration, Python/platform, point/readiness/anomalous counts,
detector total ns, runtime note, and `official_submission_ready=false`. Dataset ID/scope are
operator assertions, not automatic verification. Every run uses a new directory. Output files
are staged in a sibling temporary directory and published on success; this is single-process
publication, not a multiwriter transaction service.

AY-01 planned additive metadata: split/feature/schema versions, source revision, dirty flag,
dependency/environment digest, seed where relevant, timestamps, full timing distributions,
and workload/hardware. Current manifests must not be described as containing these fields yet.

## Config (implemented)

`configs/starter.json` uses DetectorConfig: window_size=32, min_history=8, threshold=4.0,
scale_floor=0.1, max_series=100. Require integer bounds 2<=min_history<=window_size, max_series>=1,
finite positive threshold/floor, and no unknown keys. These are starting values for wiring,
not tuned hyperparameters. Advanced model/period/quantile/guard settings must use a reviewed
separate config section or extension; do not overload threshold semantics silently.

## Truth and evaluation (implemented, provisional)

Window JSON: `{"schema_version":"1.0","windows":[{"series_id":"s","start":"...Z","end":"...Z"}]}`.
Additional top-level provenance is allowed. Windows have explicit timezone, start<=end, closed
endpoints, no overlap/touch within a series, and must fit prediction timestamp coverage.
No label file is loaded during inference.

Evaluation result: metric_id=`provisional_event_trigger_f1_v0`, official_metric=false, tp/fp/fn,
precision/recall/event_f1, per-hit delay_seconds, mean_delay_seconds (null if no hits), observation
and warmup counts, and, through evaluate_run, scope, dataset ID, input/windows hashes.
[EVALUATION](EVALUATION.md) defines exact episode matching and edge cases. Unsupported metric or
scope must error. Official benchmark/hidden scopes are not supported by this starter evaluator.

## Errors, persistence, and future adapters

`ContractError(ValueError)` reports data/config/schema violations; CLI exits 2 for expected errors.
I/O/JSON errors also produce nonzero exit. Programming errors should remain visible for diagnosis.
Do not catch exceptions and produce a fake successful score. Failed replay removes its unpublished
temporary directory. A failed run never overwrites an existing destination.

Persistence is **planned**: AY-02 proposes schema/version/config hash/series states/cursor and
last times, validates JSON types/bounds, and proves resume equals uninterrupted replay. No
checkpoint methods exist in Detector v1 yet; adding a separate StatefulDetector Protocol requires
coordination. Avoid unsafe deserialization. Whole-file deterministic replay is the current fallback.

No trainer API exists because the starter is online statistics. A future fitted comparator must
record a train-prefix manifest, expose a fit factory separate from process(), and never fit on
validation futures. Official exporter and scorer signatures are deliberately deferred until actual
schema/scoring assets exist; adapter tests should first use organizer golden examples.

## Fixture and compatibility conventions

All wiring fixtures live in tests/fixtures with explicit synthetic provenance and deterministic
values. New test doubles implement typed Protocols; do not import another contributor's unfinished
private methods. Numerical comparisons use explicit tolerances and omit elapsed_ns. Prediction
history is immutable: no later-neighbor or label-based corrections to previous records.

## Contract-change protocol

1. File a uniquely named proposal under docs/HANDOFFS with task ID, old/new examples, motivation,
   affected producers/consumers, migration/versioning, and proposed golden tests.
2. Ayush approves shared-interface changes and affected owners review. Breaking changes require
   explicit approval recorded in DECISIONS before implementation. Additive fields also need review.
3. Change typed schemas, this document, config/examples, producer/consumer tests, and migration
   together on a coordinated branch. Never merge only half of a breaking change.
4. Run baseline/contract/integration checks. Ayush updates shared state after approved integration.

Emergency work follows the same breaking-change rule; use a scoped compatibility wrapper when
possible and document human-authorized exceptions. Neither urgency nor an agent's local success
permits silently changing shared semantics.
