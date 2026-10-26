# Canonical agent entry point

Build Sentinel Pulse for Utkrishta Challenge 2. This repository carries durable context for
Codex, Antigravity, and other agents; conversation history is not a dependency.

## Read and recover context

Read [START_HERE](docs/START_HERE.md), [CURRENT_STATE](docs/CURRENT_STATE.md), your developer's
task file under `tasks/`, [INTERFACES](docs/INTERFACES.md), and relevant architecture/research.
Inspect actual `git status`, branch, recent commits, code, and tests before selecting work.
If developer identity is unknown, ask for identity before modifying owned modules.

Authority: official PDF > intended behavior in PRD/ADRs/contracts. Actual implementation is
established by Git, code/configuration, and real test results. Tasks describe ownership and
planned work; CURRENT_STATE summarizes verified integration. These are distinct kinds of truth.
Report discrepancies; never silently rewrite the architecture to match accidental code.

## Boundaries

- Ayush owns `pipeline.py`, `cli.py`, configuration, shared contracts, CI, and integration records.
- Kaustubh owns `src/sentinel/data/` and `tests/data/`.
- Manas owns `src/sentinel/detectors/` and `tests/detectors/`.
- Mayank owns `src/sentinel/evaluation/`, future `experiments/`, future `demo/`, and related tests.
- Each edits their own `tasks/<NAME>.md`; create unique handoffs in `docs/HANDOFFS/`.
- Ayush normally updates `docs/CURRENT_STATE.md`, `tasks/TASK_BOARD.md`, and `tasks/INTEGRATION.md`
  after review/merge. Other developers report updates through personal tasks/PRs/handoffs.
- `tests/test_foundation.py` is shared foundation coverage maintained by Ayush. Add new tests
  under your owned test directory. New directories should contain real work, not empty stubs.
- Breaking contracts require an impact proposal, Ayush approval, and affected-owner review
  recorded in an ADR before implementation. Major architectural changes require the same review.
- Initialization task INIT-01 may create the agreed shared foundation and all planning files.
  This exception does not authorize implementing everyone's final modules.

## Engineering rules

Python >=3.11, typed public functions, small modules, Ruff formatting. Keep the CLI independent
of UI/services. Score using only past state, emit evidence, then update. Never feed labels to
detectors, use future values, fit global scalers on validation/test, or silently substitute data.
Distinguish synthetic smoke, development validation, official benchmark, and hidden evaluation.
Do not call the provisional evaluator official. New dependencies need a reason and reviewed pins.
Do not copy public NAB labels into hidden evaluation or fetch test windows to improve a score.

## Workflow and continuity

Use one developer/task feature branch from reviewed `main`; inspect and preserve dirty work.
Never overwrite unrelated changes, automatically reset/force-push/delete branches, or merge main
without authorization. Follow [INTEGRATION](tasks/INTEGRATION.md) and
[HANDOFF_PROTOCOL](docs/HANDOFF_PROTOCOL.md). Implement assigned work, run relevant tests plus
required checks from README, and record actual commands/results. An unavailable official asset
is a blocker for the dependent step, not permission to fabricate it.

Update your task file, uniquely named handoff, and PR with changes, remaining work, tests,
dependencies, and exact next actions. Another machine can resume only committed/shared work;
say explicitly when changes are still local. Ayush reconciles shared state after integration.
Emergency fixes must be minimal, preserve evidence, notify affected owners in the PR/handoff,
and receive normal retrospective review. Exceptions require explicit human authorization and
a recorded reason; emergency status does not waive breaking-contract coordination.
