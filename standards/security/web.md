---
id: security/web
topic: security
scope: kit
status: experimental
applies_to: ["**/*"]
references: OWASP Top 10:2025 (A01 Broken Access Control and others); OWASP ASVS 5.0; dev-kit backtest (S2 permission flags hard-coded to `true`, S6 raw server text shown in a toast)
---
## Implement
- S1 When a handler reads or writes a record by id, check that the caller may access that record, not only that they are signed in. Why: object-level access is the most common access-control flaw (IDOR).
- S2 When the UI hides an action by role, the server enforces the same permission; never hard-code a permission flag to `true`. Why: client-side checks are only presentation.
- S3 When untrusted input reaches a query, a shell, HTML or a file path, use parameters or encoding at that boundary. Why: injection.
- S4 Keep secrets out of source, logs and client bundles (a web bundle or an app build). Why: anything shipped or logged is readable.
- S5 Keep personal data, medical data included, out of logs, analytics, error messages and client-side storage (`localStorage`, `sessionStorage`; in a mobile app also unencrypted device storage such as `AsyncStorage`). Why: those places are not protected like the database.
- S6 When a server error reaches the user, show a known message, not the raw server text. Why: raw text can leak internals and bypasses translation.
## Review
- S1, S2, S4 on the diff → blocker. S5 → blocker for medical data, major otherwise. S3 → blocker when reachable by a user, major otherwise. S6 → minor.
- Every security finding states the exploit scenario (rule R1, R4).
## Do not flag
- Theoretical issues with no reachable path from the change.
- Dependency CVEs when a scanner already runs in CI.
## Severity
- blocker: a user can read or change data they should not, or a secret leaks; major: exposure that needs extra conditions; minor: hardening.
