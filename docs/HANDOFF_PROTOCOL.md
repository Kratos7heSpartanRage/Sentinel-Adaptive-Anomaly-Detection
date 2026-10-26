# Persistent handoff protocol

Every substantive task handoff uses a new file under `docs/HANDOFFS/`:
`<TASK-ID>_<developer>_<YYYYMMDDTHHMMSSZ>_<short-topic>.md`. Include a suffix if needed to avoid
collisions. Never overwrite another developer's handoff. [Template](HANDOFFS/TEMPLATE.md) lists
mandatory fields. Dates are actual authored times; timezone is explicit.

Record task/developer/original owner, status, branch, shared commit/PR if available, objective,
relevant files, completed and remaining implementation, important decisions, actual commands and
results, bugs/blockers, interface dependencies, and exact next actions. Distinguish code that
exists from planned or mocked behavior. A test not run is marked not run, with reason.

For another machine to continue, the handoff must point to actual committed/shared changes and
how to retrieve them. A local commit without a remote/shared archive is still local; uncommitted
files are not accessible remotely. If sharing has not happened, say so and provide the exact
remaining sharing action. Do not invent a commit, remote URL, PR, approval, or test result.

## Producer workflow

Inspect status -> finish scoped work -> run relevant checks -> update personal task record ->
create unique handoff -> commit/push only within authorization -> reference shared commit/PR in
handoff or PR. Avoid self-referential commit hashes: write `implementation commit <hash>` from
an existing commit, and let a later handoff-only commit or PR link carry the updated record.
Ayush updates shared integration summaries after review/merge; other developers submit proposed
changes through their own task/handoff/PR. Do not compete over CURRENT_STATE/TASK_BOARD.

## Consumer workflow

Read AGENTS/START_HERE/current state/personal tasks/contracts -> inspect actual Git/code/tests ->
retrieve the referenced shared branch/commit -> compare completed/remaining work against files ->
run recorded checks -> continue the next unblocked action on an owned task branch -> produce a
new handoff. Report mismatches rather than silently treating handoff prose as executable truth.

Incomplete work must identify stable/unstable interfaces, failing tests, safe restart state, and
what not to assume. Completed work needs exact verification evidence and integration obligations.
Emergency fixes and ownership exceptions identify actual human authorization and affected owners;
breaking contracts retain the formal coordination/approval rule.
