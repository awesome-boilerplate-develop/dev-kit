# Report: <card title>

> Controller: dk:<story-runner|bug-fixer|code-refactor|pre-pr-check> · Date: <YYYY-MM-DD> · Branch: <branch> · Commits: <short SHAs>

## What changed and why
<2–5 lines; for bugs: the root cause>

## Tests
- Added: <test names>
- Red before the fix / green after: <yes/no + how checked>

## Commands run
| Command | Result |
|---|---|
| <check command> | <pass/fail, counts> |

## Review setup (required)
- Diff: <merge-base sha>...<HEAD sha> (the range reviewed)
- Depth: <self | one | four> — reason: <the C2 trigger or "small diff: N files, M lines">
- Graph: <detect-changes summary: risk, test gaps, untested functions> | "detect-changes failed: <error>" | "no .code-review-graph/ index"
- Standards applied: <ids, e.g. review/finding-quality> | none

## Review
Verdict: GO | NO-GO (from open **certain** blockers only)

### Certain findings
| Severity | Conf. | file:line | Finding (what, when it happens, impact, fix) | Rule | Status |
|---|---|---|---|---|---|
| blocker / major / minor | 80–100 | | | <rule id or —> | fixed / open / pushed back |

### Suspect findings (do not block)
| Severity | Conf. | file:line | Finding | Rule |
|---|---|---|---|---|

## Open questions and assumptions
- <anything the user should confirm; suspected bugs left as-is>
