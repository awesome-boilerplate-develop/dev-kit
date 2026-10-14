---
id: coding/review-basics
topic: coding
scope: kit
status: experimental
applies_to: ["**/*"]
references: Google Engineering Practices (code review); Fowler, Refactoring (code smells)
---
## Implement
- C1 When a call can fail (I/O, HTTP, parsing), handle the error or pass it on; never swallow it (empty `catch`, a `catch` that logs and continues as if it succeeded). Why: silent failures hide lost or wrong data.
- C2 When an async action can be triggered again before it finishes (button, retry, subscription), keep an in-flight state and release it only when the whole chain is done, follow-up reloads included. Why: releasing early lets a second trigger repeat or undo the first.
- C3 When a value can be missing (`null`, optional API field, failed lookup), give it a handling path; do not drop the record silently. Why: partial data disappears without a trace.
- C4 When the same decision already exists elsewhere (the same setting, flag or mapping), keep the new logic consistent with it, or state why it differs. Why: copies drift apart (`&&` in one place, `||` in another).
- C5 When code translates values between layers (UI names ↔ API fields, enums ↔ codes), map every value explicitly and fail loudly on an unknown one. Why: unmapped values pass through and are rejected or misread downstream.
## Review
- C1–C5 on the diff → major; blocker when data is written wrongly or lost.
## Do not flag
- Naming, formatting and anything the linter or compiler checks.
- The same pattern in code the diff does not touch.
- Missing tests (topic `testing`).
## Severity
- blocker: wrong data written or lost; major: wrong behavior a user can see; minor: harmless inconsistency.
