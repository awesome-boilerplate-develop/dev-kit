---
id: ui/forms-and-actions
topic: ui
scope: kit
status: experimental
applies_to: ["**/*.html", "**/*.tsx", "**/*.jsx", "**/*.vue", "**/*.svelte", "**/*.component.ts"]
references: WCAG 2.2 AA (1.3.1 Info and Relationships, 2.1.1 Keyboard, 3.3.1 Error Identification)
---
## Implement
- U1 Each validation message has its own condition, and each can actually appear (no message that an input mask or `maxlength` makes impossible). Why: shared or impossible conditions show the wrong message or none.
- U2 Disable or guard write actions (submit, save, delete) while their request is in flight. Why: double submits create duplicates and duplicate errors.
- U3 Every async view has a loading state and an error state the user can see; an error is not only logged. Why: silent failures look like empty data.
- U4 After a write that changes a list, reset the dependent view state (sort, paging, selection) the same way everywhere. Why: stale sort or paging shows the wrong rows.
- U5 Form fields have labels, errors are linked to their field and announced, actions work with the keyboard. Why: WCAG 2.2 AA.
## Review
- U2, U3 on the diff → major. U1, U4 → major when the user sees wrong information, minor otherwise. U5 → major on a new screen, minor otherwise.
## Do not flag
- Visual style, spacing and colors unless they break U5.
## Severity
- blocker: the user can submit or see wrong data; major: wrong or missing feedback; minor: polish.
