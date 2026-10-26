# Testing and verification strategy

Tests establish software correctness, not official detection quality. No assertion on a tiny
synthetic spike may be presented as benchmark evidence. Actual initialization commands/results
are recorded in [VALIDATION](VALIDATION.md), while this file defines ongoing expectations.

## Implemented checks

`tests/test_foundation.py` covers warmup, score-before-update evidence, threshold equality,
zero-variance protection, reset, prefix invariance, per-series isolation, cardinality bounds,
NaN/Inf rejection, timezone normalization, duplicate times, config errors, strict label-free CSV,
event episode deduplication, onset delay, pre-window triggers, empty truth/empty predictions,
window coverage/overlap, inconsistent labels, provenance/checksums, no overwrite, failed-run
cleanup, CLI errors/help, and exclusion of elapsed timing from deterministic equality.

The fixture is 16 hand-constructed points and one artificial spike. Tests install from the package,
not an implicit source-path hack. `scripts/check_repository.py` checks mandatory documents,
relative Markdown file links, and the original PDF checksum. It does not prove semantic consistency;
the initialization review and ongoing PR review must check that explicitly.

## Required contributor checks

Run owned tests for each task and the complete suite before integration. Required commands are
`python -m pytest`, `python -m ruff check .`, `python -m ruff format --check .`,
`python -m mypy`, and `python scripts/check_repository.py` inside the installed virtual environment.
Run the README synthetic CLI replay/evaluate pair after core/config/artifact changes. Use a fresh
output path. Capture actual exit codes; a PowerShell command sequence's final success does not
mean earlier checks succeeded. CI runs each command as a separate step.

## Planned tests by ownership

| Owner / directory | Required cases | Integration gate |
|---|---|---|
| Kaustubh: tests/data/ | Raw asset mapping, timezone, missingness/gaps, causal features, frozen split hashes, no overlapping training windows across split | Features match hand-derived traces; future suffix cannot change prefix frames |
| Manas: tests/detectors/ | Rolling z/MAD reference, finite scores, short/constant streams, prior-only quantiles, contaminated warmup, sustained anomaly vs benign drift | Correctness plus documented held-out ablations; no generic score-gain assertion on fixtures |
| Ayush: tests/pipeline/ | Cursor/checkpoint roundtrip, corrupted/wrong-config checkpoint, multi-series parity, no partial outputs, official export ordering, runtime collection | Uninterrupted vs resumed numerical equality and schema golden test |
| Mayank: tests/evaluation/ | Matching boundaries, duplicates, overlapping windows, no events/alerts, delay units, macro vs micro, official scorer parity, label separation | Hand-calculated golden counts agree with actual organizer scorer |
| Mayank: tests/demo/ | Parse real run artifacts, visible scope, missing files, headless core works without viewer | Offline viewer/CLI fallback rehearsal; no UI dependency in detector |

Property-style tests may use deterministic generated sequences without adding a dependency:
prefix invariance, scale/offset invariance where applicable, bounded state, output count equals
input count, and per-series permutation/interleaving invariance. Avoid tests that merely repeat
implementation lines; use independent arithmetic or invariants.

## Performance, robustness, and release checks

Record hardware/OS/Python/dependencies, window size, series count, cadence, number of points, warmup
and measured region. Warm first-call/JIT costs separately, exclude disk/plot work from detector
time, and also measure end-to-end time. Report distributions rather than a single total.
Measure peak process memory with a documented tool; starter total ns is not a p95 benchmark.

Stress malformed types/fields, huge cardinality, gaps, backwards time, long flat signals, extreme
finite values, recovery after exceptions, and output collisions. Checkpoint/export should fail
closed on incompatible versions or invalid numeric state. The synthetic stress reports are
robustness evidence, not official F1.

Before final release: fresh clone/environment reproduction, complete tests, official schema and
scorer golden cases, untouched data run, output hashes, deck count/content review, offline demo,
secret/private-asset inspection, and peer review. The configured CI matrix is Windows/Linux and
Python 3.11/3.13; only actual executed environments may be reported as verified.
