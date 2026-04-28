# Business Plan Fit Analysis

Use this workflow when the user wants to compare an announcement with a saved business
plan and decide whether the program is worth applying to.

## Inputs

- Official announcement page URL.
- Downloaded announcement attachment, preferably `pdf > hwpx > word`.
- User business plan path or user-provided business-plan text.
- Optional founder/company profile.

## Fit Dimensions

Score each dimension from 0 to 5.

- Eligibility fit: location, company age, founder age, revenue, industry, stage.
- Problem/solution fit: whether the business plan addresses the program's target area.
- Benefit fit: whether the support type is useful for the current plan.
- Evaluation fit: whether the plan already contains evidence for evaluation criteria.
- Document readiness: whether required documents can be prepared quickly.
- Risk: exclusions, relocation obligations, matching funds, IP or revenue constraints.

## Recommendation Levels

- `strong_apply`: high fit, low blocking risk.
- `apply_with_edits`: good fit but the plan needs targeted edits.
- `watch_or_prepare`: promising but not immediately ready or not currently open.
- `low_priority`: weak fit or low benefit.
- `do_not_apply`: clear eligibility mismatch or unacceptable obligation.

## Report Format

```markdown
# Fit Analysis

## Recommendation

- Level:
- Score:
- One-line reason:

## Strong Matches

## Gaps To Fix

## Risks / Disqualifiers

## Business Plan Edits

## Calendar

## Source Evidence
```

## Safety

This is decision support, not legal or accounting advice. If eligibility depends on
formal interpretation, tell the user to confirm with the program contact.
