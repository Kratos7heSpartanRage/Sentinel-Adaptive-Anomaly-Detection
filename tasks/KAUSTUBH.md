# Kaustubh - data integrity and causal time-series features

Role: data/feature engineer. Own `src/sentinel/data/`, `tests/data/`, permitted data adapters,
inventory/split manifests, and data-specific documentation. Inputs: authorized raw assets or
explicit synthetic fixtures. Outputs: validated Observation streams, FeatureFrame, provenance,
and frozen splits. Never commit restricted data or silently infer timezone/label permissions.
Read [INTERFACES](../docs/INTERFACES.md) and [EXPERIMENT_PLAN](../docs/EXPERIMENT_PLAN.md).

Status vocabulary: TODO, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE. One effort unit ~= a focused
half-day including verification; no calendar deadline or skill level is assumed.

| ID | Priority / effort | Task and explicit deliverable | Dependencies | Status |
|---|---|---|---|---|
| KS-01 | P0 / 2 | Build inventory/provenance manifest schema and validator; lengths/cadence/gaps/duplicates/finite values; audit fixtures now and real assets when received | Observation schema, fixtures | TODO |
| KS-02 | P0 / 3 | Implement bounded causal FeatureExtractor: prior median/scale, expected delta, observed delta, optional past-only seasonal reference with explicit unavailable state | FeatureFrame Protocol; no final detector dependency | TODO |
| KS-03 | P0 / 2 | Implement deterministic group/chronological split manifest tooling and boundary-purge validation; hashes and group constraints | Synthetic manifest for tests; use real inventory later | TODO |
| KS-04 | P0 / 2 | Adapt organizer starter files/labels to canonical input, with documented timezone/gap/column mapping and access provenance | Official assets and Q01/Q09 answers | BLOCKED |
| KS-05 | P1 / 2 | Real dataset EDA and train-only periodicity/cadence analysis; provide figures/notes for slides 3/5 and EXP-01 | KS-04, permitted development labels | BLOCKED |
| KS-06 | P1 / 2 | Stress feature/data behavior on missing spans, rescaling, contaminated warmup, flat/short series; report limitations | KS-02/03 | TODO |

**First three tasks:** KS-01, KS-02, KS-03. KS-01 starts on synthetic inputs with explicit labels
and cannot claim a real NAB inventory. KS-02/03 can be developed with fixed mock manifests;
do not wait for official assets to implement validation and leakage tests. Core effort: 13 units.

## Ownership and shared interfaces

Use typed Observation/FeatureFrame and explicit UTC normalization. The extractor constructs
expected statistics from earlier observations, computes current delta from the previous point,
then updates once. No centered rolling windows, global normalization, future interpolation,
whole-series period estimates, or label features. Warmup and unavailable seasonality are explicit
nulls/readiness, not invented zeros. Expose bounded history configuration through a reviewed
contract extension; coordinate shared config/type changes with Ayush and Manas.

Manas owns detection/calibration; do not tune hidden labels or independently redefine the
Prediction schema. Mayank consumes frozen split/label manifests; detector inputs exclude labels.
Manas can use fake feature frames before KS-02 is ready. AY-03 consumes the canonical stream.

## Acceptance and test responsibilities

- KS-01: correct source/checksum/time/cadence counts on a hand-derived example; missing permission,
  schema mismatch, duplicates, nonfinite values, and missing files are visible errors.
- KS-02: prefix invariance; exact known level/delta traces; scale floor; one-point/constant/short
  streams; periodic lag absent until enough past context; independent per-series state.
- KS-03: stable hashes/order; group isolation; no overlapping feature windows across training
  boundaries; reproducible split seed if needed; explicit past-context allowance at validation.
- KS-04: real sample mapping matches organizer semantics; official truth stays separate; raw
  source is unchanged; timezone assumption confirmed or explicitly unresolved rather than guessed.
- KS-05: each EDA claim identifies data/split; no test-fitted seasonality; provide actual figures
  and event counts only after authorized data is available.
- KS-06: stress results distinguish synthetic robustness from development performance; surface
  where gap handling/scale invariance fail and include integration regression tests.

Reviewer: Ayush for manifest/order/contracts and Manas for feature causality/semantics. Mayank
reviews split leakage and evaluation compatibility. Deliver tested code, example manifests,
data notes, and a unique task handoff; update only this personal task file and owned docs.

## Handoff and local progress

No KS task is complete at initialization. `data/io.py` is a strict internal reader, not the raw
NAB adapter/inventory/split/features package. Record branch, shared commit, actual commands,
results/blockers, and next actions here; follow [HANDOFF_PROTOCOL](../docs/HANDOFF_PROTOCOL.md).
Never edit shared CURRENT_STATE/TASK_BOARD concurrently with other developers.

Optional stretch: contribute past-only reference-window tooling for EXP-09/S2 after P0 tasks;
coordinate with Manas and document horizon/memory effects before adoption.
