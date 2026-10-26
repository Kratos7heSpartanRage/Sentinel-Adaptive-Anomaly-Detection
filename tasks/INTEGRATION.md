# Git collaboration and integration

Primary maintainer/final integration owner: Ayush. Each developer is an active engineer and uses
a separate clone plus task branch. The official PDF is requirements authority; PRD/ADRs/contracts
describe intent; Git/code/tests establish reality; personal tasks/board define ownership; CURRENT_STATE
summarizes verified integration. No agent assumes access to any other conversation.

## Branch and review model

`main` is the reviewed runnable integration branch. Suggested GitHub protection: PR plus one
relevant review and passing required checks. This is recommended configuration, not a claim of
existing branch protection. Create branches from reviewed main using
`feat/<developer>/<TASK-ID>-<short-name>` or `fix/<developer>/<TASK-ID>-<short-name>`.
One coherent task per branch; tightly coupled tasks may share a branch if listed explicitly.
Examples: `feat/kaustubh/KS-02-causal-features`, `feat/mayank/MY-01-event-cases`.

Before switching/starting, inspect status and recent commits. Preserve all uncommitted user work;
do not stash/reset/clean/overwrite unrelated changes automatically. Agree on an isolated branch
or separate checkout when needed. Never have all developers editing one shared working branch.

PR includes problem/outcome, task IDs, owned paths, contract impact, data/scope/metric identity,
actual tests/results, remaining work/risks, and a unique handoff. [PR template](../.github/pull_request_template.md)
is provided. Open PRs to main. Ayush reviews integration and a relevant peer reviews domain logic.
Ayush's code receives review from an affected owner; no self-approval fabrication.

## Merge gates

1. Typed contracts/config/fixtures agree, and required coordinated contract approvals exist.
2. Owned tests, complete suite, lint/format/type checks, repository checker, and affected smoke
   pass; official adapters additionally pass organizer golden cases.
3. No secret/private data/unrelated edits, leakage, fake scores, or undocumented dependencies.
4. Handoff points to shared commits/PR, with exact remaining work and verification evidence.
5. Ayush merges only with appropriate authorization; no automatic main merges, force pushes,
   destructive resets, or branch deletion. Keep merge policy simple (reviewed squash or merge).
6. After integration, Ayush reruns relevant gates and updates CURRENT_STATE/TASK_BOARD/INTEGRATION.

## Ownership and conflicts

Code ownership is in AGENTS and personal task files. Ayush is custodian of shared contracts,
build/CI, `tests/test_foundation.py`, and integrated summaries. Each developer primarily edits
their own task file and test directories. New handoffs use unique filenames; nobody rewrites
another developer's latest handoff. Planning changes proposed by others go through their own
handoff/PR rather than simultaneous shared-summary edits.

Resolve conflicts by reading both sides and the contract/official requirement. Preserve intended
behavior, rerun tests, and involve the affected owner; do not blindly accept ours/theirs or
reformat another module to simplify merging. A code/document mismatch is reported with evidence,
then fixed through review; documentation is not automatically more correct than working code.

Emergency fixes: smallest safe change in an owned branch, record incident/impact/tests and inform
affected owners through PR/handoff. A compatibility wrapper may avoid a breaking contract.
Breaking changes still need coordinated approval. Human-authorized exceptions state who/what/why
in the handoff/ADR; do not assume urgency authorizes bypassing review.

## Checkpoints and remote setup

Tag/release proposals after authorization: `foundation-v0.1`, `baseline-v0.2`, `candidate-v0.3`,
`submission-v1.0`. Names are proposed checkpoints, not existing tags. Each points to a verified
shared commit, config/split hashes, checks, and known limitations. Do not claim a release exists
before it is created.

The user specified [Manas-Jain-24/sentinel-adaptive-anomaly-detection](https://github.com/Manas-Jain-24/sentinel-adaptive-anomaly-detection)
and authorized publication. `origin` points there, and foundation `main` was pushed after checking
that no remote branches existed. Teammates follow README clone/setup instructions. The owner
still arranges contributor access and desired branch protections. Future local commits must be
pushed/shared before another computer can retrieve them. Do not place tokens in remote URLs,
config examples, committed files, or logs.
