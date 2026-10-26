# Architecture decision record

Initial decisions are proposed project design choices authorized by the initialization request;
they are not organizer rules. Ayush coordinates later changes and records affected-owner review.

| ADR | Decision / rationale | Consequence and reconsideration trigger |
|---|---|---|
| ADR-01 | CPU Python package with CLI and immutable artifacts; no required UI/service | Core works offline. Add infrastructure only for a demonstrated need and review. |
| ADR-02 | Dataclass/Protocol contracts, CSV input, JSONL/JSON internal artifacts | Portable and inspectable; official schema must be adapted explicitly, not assumed. |
| ADR-03 | C6 guarded residual system intended; C1 rolling MAD starter/fallback | Innovation is a hypothesis. Retain A if B fails measured promotion gates. |
| ADR-04 | Strictly causal prediction/thresholding and label-free inference | Prevents leakage; no hindsight seasonal filtering or score revision. |
| ADR-05 | Provisional event-trigger metric has a distinct version and official_metric=false | Enables wiring tests; official matching remains blocked until scorer arrives. |
| ADR-06 | Warmup internally NORMAL/ready=false/score=null | Avoids fake confidence, but exporter mapping needs organizer confirmation. |
| ADR-07 | One owner per subsystem; Ayush alone normally updates shared integration summaries | Limits merge conflicts; teammates communicate through personal tasks/unique handoffs. |
| ADR-08 | No official dataset substitution or benchmark claims at initialization | Synthetic fixture only tests code. Public NAB research is separately labeled if later used. |
| ADR-09 | No automatic remote creation/push/main merges or invented Git identity | Local snapshot only if existing identity permits it; human configures remote and sharing. |
| ADR-10 | Optional research libraries remain out of the required environment | Lightweight fallback; dependencies require justification, pins, platform/license review. |

## Contract and architecture change record template

Assign ADR-11 onward: task/proposal ID; date; author; problem; options; exact old/new contracts;
affected owners; evidence; migration/rollback; acceptance tests; Ayush approval and affected-owner
review reference; status. Record actual approval evidence, not a fabricated approval field.
Major changes and breaking interface changes require recorded coordination/approval. Additive
changes still need review. [INTERFACES](INTERFACES.md) gives the operational process.

## Critical review resolutions

The three adversarial reviews in [IDEA_EVALUATION](IDEA_EVALUATION.md) produced these changes:
explicit unofficial scoring identity; component/guard ablations; no guaranteed alarm-rate claim;
frozen group splits; independent core; baseline fallback; provenance in every demo; P0 official
export/scorer; and single-owner integration records. Sustained drift vs fault remains unresolved.
This review was conducted during initialization, not by claimed external reviewers or organizers.
