# Architecture blueprint

Design status: baseline path implemented; residual/calibration/adaptation/persistence/viewer are
planned. [INTERFACES](INTERFACES.md) and [DECISIONS](DECISIONS.md) define compatibility. All state
and features are local to a series; no centered/future-aware transforms or label-fed inference.

## 1. Overall architecture

```mermaid
flowchart LR
  Raw[Organizer assets] --> Adapter[Canonical adapter and manifest - planned]
  Fixture[Synthetic fixture] --> CSV[Canonical CSV reader - exists]
  Adapter --> CSV
  CSV --> Core[Sequential detector core]
  Config[Validated JSON config] --> Core
  Core --> Artifacts[Predictions JSONL and run manifest - exists]
  Artifacts --> Eval[Provisional evaluator exists / official adapter planned]
  Truth[Development truth windows] --> Eval
  Artifacts --> Export[Official exporter - planned]
  Artifacts --> View[Read-only viewer - planned]
  Eval --> View
```

The core imports no UI or evaluator. The evaluator reads saved predictions and separate truth.
Labels cannot enter the typed detector input. The viewer can fail without invalidating inference.

## 2. Processing and data flow

```mermaid
flowchart TD
  Input[Input file and declared provenance] --> Validate[Header / finite value / explicit timezone]
  Validate --> Route[Route by series ID, enforce maximum active series]
  Route --> Order[Check strictly increasing per-series time]
  Order --> Process[Score before update]
  Process --> Evidence[Label, readiness, numerical evidence]
  Evidence --> Update[Update bounded history]
  Update --> Write[Append immutable prediction record]
  Write --> Publish[On success publish run directory and checksums]
  Validate -->|invalid| Fail[Fail without final partial artifacts]
```

No resampling/imputation occurs silently. Kaustubh will implement explicit gap/missing policies
when dataset semantics are known. The starter rejects malformed rows instead of inventing values.
Routing is interleaving-safe; each series must be internally ordered. No automatic sorting of an
entire evaluation stream, which would mask upstream ordering errors.

## 3. Training and evaluation flow

```mermaid
flowchart LR
  Audit[Data provenance and inventory] --> Split[Frozen group and chronological splits]
  Split --> Fit[Train/prefix-only fitting or calibration]
  Fit --> Replay[Sequential validation replay]
  Replay --> Saved[Immutable predictions]
  Saved --> Scorer[Versioned official scorer when supplied]
  Labels[Validation windows only] --> Scorer
  Scorer --> Compare[Error analysis, delay, runtime, ablations]
  Compare --> Freeze[Freeze selected configuration and commit]
  Freeze --> Final[One untouched evaluation / organizer hidden submission]
```

The starter has no offline trainer; rolling learning occurs inside `process`. A future fitted
comparator must expose its training prefix manifest and begin evaluation without test fitting.
Calibration and unsupervised online updates use only permitted previous observations. Do not
assume organizer rules permit every update policy; record Q08 resolution first.

## 4. Intended inference flow

```mermaid
flowchart TD
  Obs[Observation t] --> History[Past-only FeatureExtractor]
  History --> Level[Level residual]
  History --> Change[Delta residual]
  History --> Seasonal[Optional validated seasonal residual]
  Level --> Combine[Fixed bounded combination]
  Change --> Combine
  Seasonal --> Combine
  Combine --> Calibrate[Threshold from prior combined scores]
  Calibrate --> Emit[Emit immutable decision and evidence]
  Emit --> Guard[Quarantine / capped influence - experimental]
  Guard --> State[Update reference and calibration state]
  Obs --> Shadow[Shadow drift statistics - experimental]
  Shadow --> Review[Bounded rebaseline policy, preserve alarm evidence]
  Review --> State
```

Starter instead uses `RollingMADStarter` directly: median of the last W values, scale
max(1.4826*MAD, floor), absolute standardized deviation, fixed threshold, then append the value.
It includes anomalous values in history and will eventually absorb persistent shifts. It has
no seasonal, empirical-threshold, quarantine, or shadow logic. That limitation is deliberate.

Level B proposal: start level/delta scores with a shared robust scale; combine by max, calibrate
the combined score using only the preceding score buffer, and test seasonal residuals separately.
Minimum quantile history and fallback must be fixed in config. A guard cannot discard data forever:
compare capped influence, finite quarantine, and an explicitly tested shadow model. Do not claim
formal alarm-rate guarantees under serial dependence or selective updates.

## 5. Module dependency graph

```mermaid
flowchart TD
  CLI[cli] --> Config[config]
  CLI --> Pipeline[pipeline]
  CLI --> Evaluation[evaluation.reference]
  Evaluation --> Data[data.io]
  Evaluation --> Pipeline
  Pipeline --> Data
  Pipeline --> Detector[detectors.rolling]
  Detector --> Config
  Detector --> Contracts[contracts]
  Config --> Contracts
  Data --> Contracts
  Pipeline --> Contracts
  Feature[data.features - planned] --> Contracts
  Residual[detectors.residual - planned] --> Feature
  Residual --> Contracts
```

Evaluation currently imports only the pipeline checksum helper, not the detector execution path.
Move common artifact helpers to an owned utility if a later change warrants it; do not introduce
an abstraction solely to remove one harmless dependency. UI/experiments remain leaf consumers.

## 6. Team integration boundaries

```mermaid
flowchart LR
  K[Kaustubh: adapters / features / split manifests] -->|Observation and FeatureFrame| M[Manas: residual detector / calibration]
  K -->|canonical CSV and provenance| A[Ayush: replay / config / artifacts / export]
  M -->|Detector Protocol and Prediction| A
  A -->|JSONL and run manifest| Y[Mayank: scorer / harness / viewer]
  Y -->|versioned reports and checks| A
  C[Shared contracts: Ayush custodian] -.-> K
  C -.-> M
  C -.-> Y
```

## Lifecycle, complexity, and deployment

One detector/extractor instance handles one series, starts empty, and may reset explicitly.
Histories are bounded by configuration. Core memory is O(SW) for S active series; median/MAD
recomputation is O(W log W) per point. With seasonal horizon H and calibration buffer C, planned
state is O(S(W+H+C)). Exact time depends on implementations and must be measured. The evaluator
holds truth windows and per-series coverage/matches; it streams JSONL and does not retain full
predictions. Reference matching scans truth windows per episode and is not the final optimized scorer.

Persistence task AY-02 will add versioned validated JSON state, config/data-cursor compatibility,
last timestamp, and replay-parity tests. Until then, recovery is a complete deterministic replay;
no `--resume` functionality exists. Models with external fit artifacts need their own reviewed
serialization contract. JSON files do not contain executable pickle objects.

Run locally with the CLI and package install. CI validates the package; no Docker, API server,
database, orchestration platform, or cloud deployment is required. A read-only local HTML viewer
is optional and consumes immutable artifacts. Inference uses no wall-clock sleeps to simulate
streaming: cadence comes from timestamps; replay speed is measured separately.
