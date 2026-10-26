# Initialization validation evidence

Task INIT-01, 2026-10-26. Environment: Windows 11, Python 3.13.5, Git 2.54.0.windows.1.
These are executed local checks. Linux/other Python CI and teammate clean-clone reproduction
have not executed. No official benchmark or hidden evaluation ran.

## Commands and outcomes

Commands use the installed virtual environment interpreter; README provides exact PowerShell paths.

| Check | Executed command (interpreter abbreviated as python) | Actual result |
|---|---|---|
| Setup | `python -m venv .venv`; venv `python -m pip install -e '.[dev]'` | Venv/package/pinned dev dependencies installed; package install repeated after README existed |
| Unit/integration | `python -m pytest -q` | 24 passed, exit 0; suite time is not detector performance |
| Lint | `python -m ruff check .` | All checks passed, exit 0 |
| Format | `python -m ruff format --check .` | 14 files already formatted, exit 0 |
| Types/imports | `python -m mypy` | Success on 12 source files, exit 0; tests/CLI also exercised imports |
| Repository | `python scripts/check_repository.py` | 32 mandatory docs, relative links, 24 unique tasks, original PDF hash passed; current link count in log |
| Dependencies | `python -m pip check` | No broken requirements, exit 0 |
| CLI help | `python -m sentinel --help` | run/evaluate commands available, exit 0 |
| Synthetic replay | README run command, final output `outputs/initialization-smoke-003` | 16 predictions, 8 ready, 1 anomalous point; manifest/evidence written; exit 0 |
| Synthetic evaluation | README evaluate command against that run and fixture windows | TP=1, FP=0, FN=0; provisional F1=1.0, delay=0 s; exit 0; software wiring only |
| Source provenance | Original PDF SHA256 | b93d18863425418a296cdbfe14335de73a69761f69d537d88fddb72b917f3ef0, unchanged |
| Secret/private-asset inspection | Token/private-key pattern scan plus intended tree/ignore inspection | No matching credential patterns; only provided PDF and synthetic data included; finite inspection is not a universal guarantee |
| Git | init main, remote/status/ignore inspection | Local main initialized, existing configured identity retained, no remote; venv/outputs ignored |

Raw logs, exact commands/exit codes, installed dependency snapshot, and synthetic output snapshots
are in [validation/](validation/). `checks.json` is machine-readable evidence. The environment
freeze excludes the editable path and is a local evidence snapshot, not a universal lock.
Synthetic JSONL elapsed ns values describe one tiny run, not an efficiency claim.

## Issues found and corrected

First run: 23 tests passed. Ruff found long lines, UTC alias style, and an unspecified zip strict
argument; fixed and formatted. Review found possible floating-point overflow with extreme finite
inputs; the starter now raises ContractError instead of emitting nonfinite scores, with a dedicated
test. Malformed timestamp/series types reject explicitly. Added task-ID checks and portable LF
rules for CSV/JSONL. Staging review exposed Windows newline normalization of prediction snapshots;
the writer now emits LF on every platform and a regression assertion checks it. Synthetic artifacts
were regenerated for the final snapshot. Final checks passed after these changes.

## Semantic review

Reviewed PDF pages 1-3, rubric arithmetic, six concepts/risk deductions, delivery-level boundaries,
six diagrams versus source imports, typed/config/artifact/evaluation contracts versus code,
24 tasks/ownership/effort (13 planned units each), and first-three-task readiness. No reviewed
document contradiction remains unresolved. Organizer ambiguities remain explicit questions.

Key checks: the 15-run cap is Challenge 1 only; no official scorer/schema claim; null warmup and
episode-trigger semantics are consistent; advanced detectors/calibration/guards/checkpoints/UI
are planned; MAD includes anomalies in updates; all four own significant engineering work;
Ayush reconciles shared summaries; no remote/push/submission is claimed.

## Fresh-agent onboarding simulation

This was a repository-only walkthrough during initialization, not a claimed separate agent run.

| Required action | Repository evidence / walkthrough result |
|---|---|
| Understand project/official problem | README -> START_HERE -> original PDF/PROBLEM_ANALYSIS; all source pages available |
| Understand intended solution | PRD, IDEA_EVALUATION, ARCHITECTURE, DECISIONS; starter vs final explicit |
| Identify identity/ownership/tasks | AGENTS and personal task files; 24 unique IDs verified |
| Find actual completed/incomplete work | CURRENT_STATE compared to src/tests/Git; all developer extensions remain TODO/BLOCKED |
| Discover contracts | INTERFACES, contracts.py, config; coordinated change process explicit |
| Find next unblocked task | First three tasks per owner, typed doubles/fixtures and dependencies specified |
| Follow Git workflow | INTEGRATION: own clone/branch, dirty-work preservation, PR/review, no destructive automation |
| Resume a handoff | HANDOFF_PROTOCOL/template require actual shared changes; local-only limits explicit |
| Run checks | README commands installed/executed locally, actual results recorded |
| Document changes/prepare integration | Personal tasks + unique handoff + PR template; Ayush reconciles shared summaries |

G0 initialization acceptance is satisfied. M1-M3 artifacts exist; M4/G1, valid Level A (G2),
measured B, final deck/demo, and submission remain incomplete. The INIT-01 handoff and actual
history identify local snapshot commits. Another computer requires a real sharing step.
