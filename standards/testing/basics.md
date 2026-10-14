---
id: testing/basics
topic: testing
scope: kit
status: experimental
applies_to: ["**/*"]
references: Beck, Test-Driven Development by Example; Google Testing Blog (test behavior, not implementation)
---
## Implement
- T1 A bug fix comes with a test that fails before the fix and passes after, at the level where the bug was seen. Why: it proves the fix and keeps the bug from coming back.
- T2 A test of an error branch asserts the specific outcome (message, state, call arguments), so it fails when the branch breaks. Why: "was called" assertions pass while the behavior is wrong.
- T3 Test behavior through the public interface, not private details or mocks of the unit under test. Why: such tests break on refactors and miss real bugs.
- T4 Never skip, delete or weaken a test to get green; if a test is wrong, fix it and say why. Why: a lowered bar hides regressions.
## Review
- T1 missing on a bug fix → major. T2 (a test that passes while the code is broken: say how) → major. T4 → blocker.
## Do not flag
- Missing tests for code the diff does not change; a coverage percentage on its own.
## Severity
- blocker: the bar was lowered (T4); major: a fix or branch is not really tested; minor: test style.
