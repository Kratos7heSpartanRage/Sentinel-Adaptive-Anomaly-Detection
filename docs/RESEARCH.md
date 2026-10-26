# Technical research log

Reviewed 2026-10-26. Sources below are primary papers, author repositories, or official library
documentation. These are research findings, not measurements of our system. No third-party
leaderboard number is used as an expected hackathon score. Licenses/versions must be checked
before incorporating external implementation code; none is copied into this starter.

| Source | Research-backed finding | Design implication / limits |
|---|---|---|
| [R1: NAB repository](https://github.com/numenta/NAB) | NAB supplies streaming time series, labels, and its own scoring procedure. | Use provenance-aware adapters; the prepared hackathon subset may differ. Public NAB is not the organizer data. |
| [R2: NAB original paper](https://arxiv.org/abs/1510.03336) | Evaluation explicitly incorporates temporal anomaly windows and timing. | Event semantics matter. Hackathon event F1 must not be replaced with NAB's normalized score. |
| [R3: Rigorous TAD evaluation, Kim et al.](https://arxiv.org/abs/2109.05257) | Point adjustment can inflate reported F1 and obscure detector quality. | Preserve original outputs; do not expand flags retrospectively with ground truth. |
| [R4: Siffer et al., SPOT/DSPOT paper](https://www.amossys.fr/wp-content/uploads/anomaly-detection-with-evt-1.pdf) | EVT tail modeling supports stream thresholds; stationary and drifting cases require different treatment. | Tail fitting is a candidate, not a distribution-free false-alarm guarantee for arbitrary dependent residuals. |
| [R5: River ADWIN](https://riverml.xyz/dev/api/drift/ADWIN/) | Adaptive subwindow comparisons detect distribution change; checking frequency affects delay. | A drift signal can inform a shadow model. It cannot tell benign drift from a real anomaly. |
| [R6: IsolationForest API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) | Isolation Forest provides outlier scores and a contamination-related decision offset. | Benchmark causal lag/residual features; orient scores consistently and tune on validation only. Batch fitting is not inherently online adaptation. |
| [R7: Matrix profile author paper](https://www.cs.ucr.edu/~eamonn/MP_journal.pdf) | Matrix profiles support motifs and discord discovery through subsequence similarity. | Strong shape-anomaly comparator; subsequence length and reference-history policy matter. |
| [R8: STUMPY streaming tutorial](https://stumpy.readthedocs.io/en/latest/Tutorial_Matrix_Profiles_For_Streaming_Data.html) | Incremental profile updates and finite-window egress are available; old scores can change as new neighbors arrive. | Freeze emitted historical decisions. Use a left/past-only reference to prevent hindsight leakage. |
| [R9: Author-maintained libspot](https://github.com/asiffer/libspot) | C implementation and bindings target stream outliers; repository exposes LGPL-3.0 licensing. | Optional stretch dependency; check platform/build/license obligations before adoption. |

## Fundamental method comparison

Robust rolling statistics give immediate evidence and no training dependency. Median/MAD resist
isolated contamination but a sustained shift eventually enters the reference window. Raw z-scores
can overreact to seasonal peaks, underreact after variance inflation, and fail on zero variance.
Use a positive scale floor and separately inspect warmup/constant signals.

Forecast residuals isolate deviations from expected seasonal/trend behavior. A seasonal-naive
prediction must use a lag already observed, with period estimation from a permitted past prefix
only. When the prefix cannot establish stable periodicity, use the nonseasonal predictor.
Residual quality, not model complexity, determines detection quality; prediction error alone can
miss abnormal variance or repeated low-amplitude shifts. Include a change component only if an
ablation demonstrates value. These are design inferences from temporal modeling, not proven gains.

Isolation Forest on trailing statistics captures multifeature departures but needs refitting,
can learn temporal context poorly without features, and adds score-calibration complexity.
LOF novelty mode and One-Class SVM are alternative comparators; neighbor/state or kernel cost
can exceed a bounded-statistics detector. Neither is assumed superior without local experiments.

Matrix profiles are useful for unusual shapes; z-normalization can hide absolute level anomalies,
and a new regime may remain novel for many windows. Compare bounded past-history distance plus
a level detector. Avoid citing constant update cost independent of the reference horizon:
practical cost depends on the maintained history and implementation.

Autoencoders or sequence forecasters could model nonlinear patterns, but training contamination,
few development events, window latency, score calibration, and CPU inference raise risk. A causal
small 1D convolutional autoencoder remains a comparator/study, not the default dependency.

## Chosen hypotheses to test

- H1: Combining robust level and first-difference residuals reduces missed short events relative
  to a single level score at an acceptable false-positive rate.
- H2: A validated past-only seasonal reference reduces false alerts on periodic series.
- H3: Past-score empirical quantile calibration transfers across series better than one raw
  threshold. Dependent streams and anomaly contamination invalidate naive probability claims.
- H4: An anomaly quarantine plus shadow drift tracker reduces long alert storms without erasing
  true sustained events. This tension is unresolved; thresholds and reset policy need ablation.

These are **unmeasured engineering hypotheses**. A max of several scores increases opportunities
for false positives; calibrate the combined score, do not independently threshold each branch
and assume the ensemble preserves an alarm rate. Guarding updates also biases calibration and
can freeze adaptation; compare no guard, capped influence, and bounded quarantine.

## Generalization and reliability

Hold out complete series when possible and use chronological folds inside development series.
Group related files by origin to reduce near-duplicate leakage. Store split manifests before
tuning. Never optimize against hidden windows, rescale using future data, or choose a seasonal
period using the whole evaluation trace. Report per-series failures, event counts, and delay,
not only an average. Short series, irregular cadence, gaps, flatlines, and contaminated warmup
are mandatory stress cases. Exact official aggregation remains an organizer question.

## Open-source adoption shortlist

NAB: inspect schema/methodology, avoid importing its legacy execution stack into core.
scikit-learn: optional IF/LOF/OCSVM experiments behind extras after version pinning.
STUMPY: optional causal shape comparator, with first-call compilation time reported separately.
River: optional drift experiment, preserving detector semantics.
libspot: optional EVT calibration study with license/build review. The starter installs none
of these; a standard-library path keeps collaboration and fallback execution simple.
