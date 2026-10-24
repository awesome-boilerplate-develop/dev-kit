# Step 8: the `CONSTRAINTS.md` question

Read at step 8 before asking it (a detailed setup, and the project has no `CONSTRAINTS.md` of its own).

## What the question must explain

The question must explain itself, in the user's language, filled in with what step 3 found:

- **What it is:** a written quality bar for *how good a change must be before it ships*, as numbers, each with the command that checks it (for example "zero type errors: `tsc --noEmit`", "changed lines ≥ 80% covered", "no high security findings: `semgrep`"), plus a floor that always applies (no new suppressions such as `@ts-ignore`, no stubs, no skipped or deleted tests, no secrets) and a list of agreed exceptions.
- **How it differs from the standards just chosen:** standards say *how code in this repo is written* (rules the agent cannot guess, used while coding and reviewing); `CONSTRAINTS.md` sets the *pass bar and the tools that measure it*, and exists so the agent cannot quietly lower the bar to get green.
- **What the user already has without it:** `dk:pre-pr-check` already flags new skips, suppressions, deleted asserts and weakened thresholds in the diff; list the checks the repo already runs (type checker, linter, coverage, CI gates) from step 3.
- **What it would add here:** the dimensions that are missing from that list (for example "no linter and no coverage gate today").
- **Cost:** up to 4 more questions (which dimensions, block or warn, target numbers or "measure today and hold", slowest acceptable check); possibly installing a tool, always asked first; its benefit has not been measured in the dev-kit lab.
- **Where and who reads it:** `.dev-kit/CONSTRAINTS.md`, personal and never committed; `dk:pre-pr-check` step 1 reads it, and a change that breaks it is a blocker.

## Answer

"no" (default; nothing is lost, the floor checks above still run) or "yes".
