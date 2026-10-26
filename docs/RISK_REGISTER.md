# Risk register

Likelihood/impact are planning judgments (L/M/H), not measured probabilities. Ayush reviews P0
risks at integration checkpoints; each owner records evidence in personal tasks/handoffs.

| ID | Risk / likelihood / impact | Early signal | Mitigation and fallback | Owner |
|---|---|---|---|---|
| R01 | Missing official assets / H / H | No starter pack in workspace | Obtain authorized assets; build only wiring using clearly synthetic fixtures | Kaustubh |
| R02 | Wrong event metric / H / H | Matching/warmup/dedup unknown | Official scorer parity before claims; retain explicitly provisional local metric | Mayank |
| R03 | Invalid submission schema / H / H | Output columns/order absent | P0 exporter after schema; validate organizer golden file; do not submit internal JSONL blindly | Ayush |
| R04 | Temporal/label leakage / M / H | Whole-series scaler or revised old scores | Prefix tests, group splits, independent label-free replay; reject contaminated results | All |
| R05 | Threshold overfitting / H / H | Few events, per-file label tuning | Small predefined search, held-out groups, counts/uncertainty; simple baseline fallback | Manas/Mayank |
| R06 | Learning persistent fault as normal / H / H | Alert disappears during sustained fault | Guard/no-guard/shadow ablations; preserve raw baseline and event recall | Manas |
| R07 | Guard freezes adaptation / M / H | Permanent alert storm or stale calibration | Bounded quarantine/capped influence, shadow evidence; disable guard if no gain | Manas |
| R08 | Irregular cadence/naive timezones / M / H | Missing spans/ambiguous local times | Explicit adapter and gap policy; reject assumptions until resolved | Kaustubh |
| R09 | Runtime/memory surprises / M / M | Increasing series/horizon/JIT cost | Bound state, profile p95/cold start; remove expensive branch | Ayush |
| R10 | Parallel schema/summary conflicts / M / H | Divergent output formats, shared doc edits | Canonical types, ownership, proposal process, unique handoffs | Ayush |
| R11 | UI/demonstration failure / M / M | Missing browser/library/network | Artifact-only viewer, offline CLI/video fallback | Mayank |
| R12 | Untested remote/platform / M / M | Local passes but CI unavailable | Record actual environment, CI matrix, teammate clean-clone reproduction | Ayush |
| R13 | External dependency/license burden / M / M | Optional library lacks target build | Pin/review; no code copied; omit optional method | Relevant model owner |
| R14 | Synthetic example mistaken for benchmark / M / H | High toy F1 shown without provenance | Scope/metric/data labels on report and demo; no official score until evaluated | Mayank |
| R15 | Unknown deadline/resources / H / M | Schedule and hardware not provided | Relative estimates and priority gates, baseline first | Ayush |

If official assets cannot be obtained, the foundation can still be delivered, but Level A cannot
be claimed as a valid competition submission. Do not resolve that risk by relabeling public or
synthetic data. Open organizer questions remain visible in CURRENT_STATE and release checklist.
