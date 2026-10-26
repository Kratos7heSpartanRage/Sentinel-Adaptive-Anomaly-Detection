# Integrated task board

Primary maintainer: **Ayush**. Other developers update their personal task files and unique
handoffs; Ayush reconciles this board after reviewing/merging evidence. No assigned implementation
task below is marked done merely because a starter for its subsystem exists.

| Workstream | Ready first tasks | Later tasks | Externally blocked |
|---|---|---|---|
| [Ayush](AYUSH.md) | AY-01, AY-02 proposal, AY-03 | AY-05, AY-06 | AY-04: official schema/entrypoint |
| [Kaustubh](KAUSTUBH.md) | KS-01, KS-02, KS-03 | KS-06 | KS-04/05: starter assets/timezone/labels |
| [Manas](MANAS.md) | MN-01, MN-02 with fake features, MN-03 unit tests | MN-04, MN-06 after gates | MN-05: permitted data/harness |
| [Mayank](MAYANK.md) | MY-01, MY-02 with starter runner, MY-03 | MY-05 preparation | MY-04: scorer; MY-06: frozen results |

All 24 task statuses/effort/dependencies are in the personal files. **INIT-01 is DONE** for the
foundation scope; verified completion and exact checks are recorded in CURRENT_STATE/VALIDATION.
No official-data experiment or submission milestone is complete.

First integration target: **M4 / G1** in [MILESTONES](MILESTONES.md): causal baseline plus one
residual path, manifests/splits, event golden tests, reproducible comparison, CLI/optional viewer.
P0 official-data adapter/scorer/export run in parallel when assets arrive; G2 is the actual valid
fallback submission gate. Use TODO -> IN_PROGRESS -> IN_REVIEW -> DONE with BLOCKED plus reason
when genuinely dependent on missing input. Include handoff and PR references when statuses change.
