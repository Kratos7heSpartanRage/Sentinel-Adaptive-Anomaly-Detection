# Demo built around evidence

Owner: Mayank, with Ayush on the CLI and Manas/Kaustubh supplying genuine model/data evidence.
The live objective is immediate clarity: a stream arrives, past context defines an expectation,
an observation deviates, and a scored alert explains its numerical cause. Show the same artifacts
the evaluator/exporter consume. Do not turn a synthetic spike into a benchmark performance claim.

## Proposed short sequence (duration is a design choice)

1. In about 20 seconds identify Challenge 2, dataset provenance, and the selected run/config/metric.
2. Replay a small authorized development trace through the CLI. No artificial pauses are needed
   for speed measurement; optional visual pacing must be excluded from inference timing.
3. Inspect one true detected event: show value, prior expected level, scale, residual/components,
   actual threshold and trigger timestamp. Explain why the value crossed the threshold.
4. Compare the simple baseline to the selected candidate on identical frozen inputs and scorer.
   Show event counts/F1, precision/recall, delay with misses, and measured runtime/hardware.
5. Show one false positive or missed event and its likely statistical limitation. Avoid claiming
   an underlying physical cause that a univariate detector cannot establish.
6. Finish with reproducible commands, schema-valid predictions, and the offline fallback.

Before real assets exist, demonstrate only the saved synthetic fixture and visibly label it
`synthetic_smoke / software wiring only / provisional metric`. Do not fill real-result charts
with illustrative values. Hidden test windows are never displayed unless organizers authorize it.

## Optional viewer design (MY-03, not implemented)

| Screen | Content | Interaction / correctness constraint |
|---|---|---|
| Run overview | Dataset/scope/metric/scorer/config/revision, event counts, runtime context | Select a saved run; refuse incompatible schema; missing labels shown as unavailable |
| Trace inspector | Value, available expected baseline, flagged timestamps, permitted truth windows | Pan/select an event; distinguish model alerts from truth; no retrospective score edits |
| Evidence panel | Pre-update baseline, scale, residual, branch scores, threshold, readiness | Selecting a point reads its actual JSONL record; warmup visibly unavailable |
| Comparison/errors | Paired baseline/candidate metrics, misses/FPs, delay and speed | Same split/scorer only; export traceable chart/table; show count denominators |

A static offline HTML/SVG viewer is enough; no API server/database/authentication flow is needed.
Never require the viewer to produce predictions or export the official submission. It consumes
read-only artifacts. Display units and actual measured timing boundaries. If no final timings
exist, show unavailable rather than a mocked speed number.

## Failure fallback and rehearsal

If the viewer fails, run the README CLI replay/evaluate commands and inspect saved JSONL evidence.
If live data access fails, use a previously reproduced, authorized, checksummed development run,
clearly stating it is saved. Keep a short local video/screenshots and the environment setup ready.
If official schema/scorer is still missing, say so; internal output is not proof of submission validity.

Rehearse offline from a shared commit with a clean environment. Verify synthetic vs development
labels, chart units, evidence arithmetic, baseline parity, false-positive example, and exactly
10 slides. All four members should explain their subsystem and its limits in Q&A. Record actual
rehearsal results under a MY-05 handoff, not a generic 'demo passed' claim.
