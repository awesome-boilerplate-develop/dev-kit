---
id: review/finding-quality
topic: review
scope: kit
status: experimental
applies_to: ["**/*"]
references: Codex review rubric (openai/codex); Claude Code code-review plugin; claude-code-security-review
---
## Review
A finding may be reported only if all of these hold:
- R1 It is introduced by this change (in the diff), not pre-existing elsewhere.
- R2 It is discrete and fixable, and the author would want to fix it if they knew.
- R3 You can point to what is affected (file:line, the caller or flow); no "might break something" without naming it.
- R4 You state when it happens: the input, scenario or environment (for security: the exploit scenario).
- R5 It is not an intentional change that serves the purpose of the PR.
- R6 It is not in the topic's "Do not flag" list, and not something lint, typecheck, compiler or CI already catches.
- R7 If it rests on a rule, cite the rule id (for example `team-a/ui-controls#U1`) and the file it comes from.

Each finding carries a confidence from 0 to 100 and goes in one of two tiers:
- **Certain** (confidence ≥ 80): you verified it against the code. Counts toward the verdict; an open certain `blocker` means NO-GO.
- **Suspect** (50–79): a plausible problem you could not fully verify. Listed separately, never blocks the merge.
- Below 50: drop it.

Write each finding as one short paragraph: what is wrong, when it happens, the impact, and the fix. Do not overstate severity; no praise or filler.

## Do not flag
- Style, formatting and naming the repo's linter already enforces.
- Pre-existing issues on lines the diff does not touch.
- "Missing tests" in general, unless a rule or the spec requires them for this change. A test that exists but passes while the code is broken (no assertion, asserts nothing specific, passes vacuously) is a defect, not a missing test: say how it still passes.
- Speculation about other parts of the code you have not identified.
