# Implementation sequence and integration gates

INIT-01 establishes researched requirements, contracts, a runnable starter, task ownership,
and verified continuity. This initialization does not finish all four workstreams. Actual status
is in [CURRENT_STATE](CURRENT_STATE.md), personal tasks, and [milestones](../tasks/MILESTONES.md).

## Immediate parallel work

| Developer | First three tasks | Shared input available now | Handoff output |
|---|---|---|---|
| Ayush | AY-01 run/profiling metadata; AY-02 state persistence; AY-03 replay/error parity | Detector Protocol, JSONL, config, fixtures | Replay runner/state proposal, tested artifacts |
| Kaustubh | KS-01 inventory/manifest validation; KS-02 causal features; KS-03 frozen splits | Observation/FeatureFrame contracts, synthetic data | Auditable manifests, extractor, split tests |
| Manas | MN-01 rolling z comparator; MN-02 residual components; MN-03 prior-score thresholds | Detector/FeatureExtractor Protocols, fake frames, fixtures | Detectors/calibration with causal tests |
| Mayank | MY-01 event golden suite; MY-02 experiment harness; MY-03 artifact viewer | JSONL/run.json and provisional metrics | Matching tests, run comparison, scope-labeled viewer |

These can begin without official data using contract doubles and clearly synthetic fixtures.
Within each workstream later tasks depend on its own earlier work. Cross-stream integration
uses typed contracts; do not block Manas on a finished KS-02 extractor or Mayank on a final model.
Official-only tasks stay blocked until their actual dependencies arrive.

## Gates

G0 foundation: docs/ownership/contracts, install/import/test/lint/type/smoke verified and actual
local/remote Git state recorded. G1 baseline integration (M4): two detectors, causal features,
manifest/split validation, independent replay, event golden tests, comparison artifacts, and viewer
or CLI evidence. G1 may prove wiring synthetically; permitted real-data replay is required once
available and must be reported separately.

G2 valid Level A: KS-04 official input adapter, MY-04 official scorer, AY-04 official export,
warmup/order/schema clarification, real permitted evaluation, README, baseline deck/demo coverage.
This is the guaranteed-fallback target; initialization is not G2.

G3 candidate B: residual/quantile/adaptation components pass ablations, promotion gates, robustness
and runtime checks on held-out groups. G4 release: official schema acceptance, frozen code/config,
untouched result, exact 10 slides, working offline demo, submission audit and shared handoffs.

## Scope and sequencing discipline

Prioritize P0 correctness/evaluation/export before P1 complexity and P2 research. Individual
effort estimates are relative; no hackathon end date or developer expertise has been assumed.
No dashboard task can block core submission. Every PR has one coherent task or closely coupled
task set, explicit contract impact, actual verification, and an integration owner/reviewer.

When official requirements arrive, compare them to assumptions, update traceability/ADRs and
affected contracts with review, then run baseline parity before advanced experiments. Do not
rewrite all modules to satisfy a guessed schema. Risks and fallback decisions are explicit in
[RISK_REGISTER](RISK_REGISTER.md) and [EXPERIMENT_PLAN](EXPERIMENT_PLAN.md).
