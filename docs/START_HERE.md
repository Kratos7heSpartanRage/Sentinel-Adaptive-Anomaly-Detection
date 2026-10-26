# Joining Sentinel Pulse

The project targets the official Sentinel streaming anomaly challenge. Read the
[official PDF](<../Utkrishta 2026 Participant Problem Statements.pdf>) completely; page 2 is
Challenge 2 and page 3 defines common deliverables. Page 1's 15-run budget is Challenge 1 only.

## Source-of-truth hierarchy

| Question | Source |
|---|---|
| What does the competition require? | Official PDF; requirement IDs in [traceability](REQUIREMENTS_TRACEABILITY.md) |
| What should our system do? | [PRD](PRD.md), [ADRs](DECISIONS.md), [contracts](INTERFACES.md) |
| What actually exists/works? | Git history, source/configs, and tests actually executed |
| Who owns planned work and status? | Individual `tasks/` files and Ayush-maintained [board](../tasks/TASK_BOARD.md) |
| What has been integrated and verified? | [CURRENT_STATE](CURRENT_STATE.md), checked against actual code |

Read [AGENTS](../AGENTS.md), CURRENT_STATE, [architecture](ARCHITECTURE.md), interfaces, then
your personal file: [Ayush](../tasks/AYUSH.md), [Kaustubh](../tasks/KAUSTUBH.md),
[Manas](../tasks/MANAS.md), or [Mayank](../tasks/MAYANK.md). The team has no assumed experience ranking.

## First session on any coding agent

1. Supply your developer identity and task ID using [AGENT_PROMPTS](../tasks/AGENT_PROMPTS.md).
2. Inspect `git status --short --branch`, `git log -5 --oneline` (if commits exist), and your
   module/tests. Preserve existing local changes. Summaries are navigation, not proof of completion.
3. Create a separate task branch from reviewed main. Use your own clone on your computer.
4. Run README setup and the relevant existing tests. Check [VALIDATION](VALIDATION.md) for prior evidence.
5. Work on your next unblocked task. The first three tasks in each personal file can start using
   typed contracts and synthetic fixtures; real data performance remains blocked by official assets.
6. Validate, update your personal task record, and create a unique handoff. Commit/share changes
   before claiming another machine can continue them. Open a PR and ask the listed reviewer.

The implemented path is CSV -> RollingMADStarter -> JSONL/manifest -> provisional event F1.
This is a foundation, not the intended competitive residual ensemble. Code under `src/` is real;
future feature extractors, advanced calibration, checkpointing, official export, and UI are plans.

## First shared integration target

M4 combines KS-01/02/03, MN-01/02/03, MY-01/02/03, and AY-01/02/03: manifest-backed replay of
baseline and one residual candidate with checked contracts, a reproducible experiment report,
and a synthetic wiring demo. It must also run on permitted development data once supplied.
Official submission compliance remains blocked until MY-04 and AY-04 resolve the scorer/schema.
See [milestones](../tasks/MILESTONES.md), [experiment plan](EXPERIMENT_PLAN.md), and
[organizer questions](QUESTIONS_FOR_ORGANIZERS.md). No hackathon deadline has been assumed.
