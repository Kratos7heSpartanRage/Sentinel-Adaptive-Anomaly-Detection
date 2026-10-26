# Submission checklist

Owner: Ayush coordinates; each owner supplies evidence. Check items only when actually completed.
Initialization creates the foundation, not the final competition package.

## P0 official assets and semantics

- [ ] Authorized organizer NAB subset/starter pack recorded with provenance/hashes (KS-04).
- [ ] Development versus hidden windows and permitted training/online updates confirmed (KS-04).
- [ ] Official event matching, warmup, duplicate/overlap policy, averaging, and delay units confirmed (MY-04).
- [ ] Official scorer version and golden examples reproduced (MY-04).
- [ ] Prediction schema, row order, labels, score/warmup representation, file names confirmed (AY-04).
- [ ] Runtime hardware/boundaries, entrypoint/dependency restrictions, deadline/submission channel confirmed.

## P0 reproducible code and predictions

- [ ] Valid Level A baseline remains runnable without UI/services.
- [ ] Final model chosen using frozen permitted splits and promotion gates; no hidden-label tuning.
- [ ] Required tests, lint/format/type/repository checks and schema golden cases pass from shared commit.
- [ ] Final source/config/dependency/data/split/output hashes and actual hardware are recorded.
- [ ] Official-format prediction file validated, with score/label/evidence obligations satisfied.
- [ ] Clean-clone README setup and final run reproduced on a teammate's computer.
- [ ] No secrets, restricted datasets, fake results, unrelated work, or unsafe serialized objects included.
- [ ] Source code/notebooks and README satisfy PDF p3: environment, strategy, reproduction instructions.
- [ ] Final untouched local result is labeled accurately; only actual organizer output is called hidden score.

## P0 presentation and demonstration

- [ ] Exactly 10 slides follow every row of PRESENTATION_PLAN.
- [ ] Actual representation/windowing/adaptive threshold and experiment trajectory explained.
- [ ] Precision/recall/event F1/delay/runtime use correct scope/metric/units and traceable artifacts.
- [ ] True event plus false-positive/miss analysis and numerical evidence shown.
- [ ] Team name/members/track, limitations, and conclusion included.
- [ ] Brief live/video demo works offline; saved artifacts/CLI/video fallback rehearsed.
- [ ] All four contributors can explain their code/contracts and answer evaluation/leakage questions.

## Release handoff

- [ ] Reviewed source commit/remote shared, task statuses reconciled by Ayush.
- [ ] CURRENT_STATE and unique release handoff match actual integrated tests/artifacts.
- [ ] Release/tag/merge/push actions have appropriate authorization; no automatic destructive Git actions.
- [ ] Submission made through the actual organizer channel, with receipt if available.

The initialization evidence lives in VALIDATION, separate from this unchecked final checklist.
No submission has been made, no final deck exists, and no official score is available at foundation time.
