# Step 7: writing the standards

Read before writing any standards file, after each read-back the user approved.

**Write, after each read-back.**

## Items

Turn kept items and free-text answers into items in `${CLAUDE_PLUGIN_ROOT}/templates/standard.md` format: one idea per item with an ID, a trigger ("When X, …"), a one-line why and a severity. Say so when an answer breaks principle 0 (the agent already knows it, or a linter checks it) and suggest not writing it.

## IDs

- Decide the topic file of an item when you first show it, and take its ID from that topic: one letter and a number, unique in the file, never changed afterwards.
- Rules (`## Design`, `## Implement`) use the topic's letter: `A` architecture, `C` coding, `T` testing, `S` security, `U` ui (in-house component libraries included), `P` api, `D` data, `O` ops, `R` process. A review-only check uses `V`. `## Do not flag` lines need no ID.
- A date-handling convention is coding (`C`), not data; data means stored data, schemas and migrations.

## Where items go

- Pass-1 items under `## Design` or `## Implement` of the topic file the rule is about; pass-2 items under `## Review`, `## Do not flag` and `## Severity` of the topic file of what they check: environment, pipeline, deployment and dependency files go to `ops/`, translation files to `ui/`, exposed module contracts to `architecture/`.
- Create that topic's file if needed; never put a check into a file only because it is open.
- Repo items → `.dev-kit/standards/<topic>/<name>.md`, with `id: <topic>/<name>` matching the path, `status: experimental` as in the template (a repo rule is not measured yet), and the file `id` and item IDs exactly as shown in the read-back.
- Kit files kept in either pass → `standards.kit`; switched-off kit items → `standards.disable`.

## Check what you wrote

From the repo root run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_standards.py`. It checks the frontmatter (`id` matches the path, `topic`, `scope`, `status`), that every `applies_to` glob matches a tracked file, the section names (each at most once), and the IDs (format, unique, every ID a Review line names is defined).
- If it prints FAIL lines, fix the files and run it again (at most 3 times); if it still fails, say so in the report.
- Put its last output in `init-report.md`.
