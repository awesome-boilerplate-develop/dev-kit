# Graph playbook (rule G1)

Use only when the index exists: `.codegraph/` for codegraph, `.code-review-graph/` for code-review-graph (CRG). No index → skip, use grep/read as usual.
CLI only. CRG prints JSON: always reduce it with `jq -r '.summary'` (or the field you need); never paste raw output into reports.
`<base>` is `base_branch` from `.dev-kit/config.yml` (default `main`).

## §1 Freshness (once per session, before the first query)
If a tool is not on PATH, `bash <dev-kit root>/scripts/install-graph-tools.sh --check` (the dev-kit root is the folder that contains this `rules/` folder) prints its absolute path; call it by that path for the rest of the session (no reload needed — dev-kit uses the CLI, not MCP).
- `codegraph sync`
- `code-review-graph update -q`

## §2 Locate code
- Question or area: `codegraph explore "<symbols or question>" --max-files 5`
- One symbol with its callers/callees: `codegraph node <symbol>`
- Who calls / what it calls: `codegraph callers <symbol>` · `codegraph callees <symbol>`
- Trace a symptom backwards (debugging): start at the failing function, follow `codegraph callers` up to where the bad value is produced.

## §3 Blast radius before changing existing code
- One symbol: `codegraph impact <symbol> -d 2`
- Files you will touch: `code-review-graph impact --files <f1> <f2> --depth 2 | jq -r '.summary'`
- Subclasses that inherit the behaviour: `code-review-graph query inheritors_of "<file>::<Class>" | jq -r '.results[].name'`

## §4 Existing tests (where to add a test, what to run first)
- Python/any: `code-review-graph query tests_for "<file>::<Class.method>" | jq -r '.results[].name'` (use the qualified name; if it says "ambiguous", pick from `.candidates`)
- JS/TS: `git diff --name-only <base> | codegraph affected --stdin -q` (in the lab it found nothing for Python — do not rely on it there)
- Run the tests found here first, then the full check command.

## §5 Refactor support
- Candidates: `code-review-graph large-functions --path <dir> --min-lines 50 | jq -r '.summary'`
- Characterization targets: §4 `tests_for` on every public symbol you will move; untested ones get characterization tests first.
- Rename preview (lists every edit site, changes nothing): `code-review-graph refactor rename --old-name <old> --new-name <new> | jq -r '.summary, (.edits[] | "\(.file):\(.line)")'`
- Before deleting code: `code-review-graph dead-code --file-pattern "<path>" --limit 20`

## §6 Large work (story/refactor through plans)
- Module map for placing new code: `code-review-graph architecture --detail-level minimal | jq -r '.summary'`
- Cohesive areas: `code-review-graph communities --min-size 5 --sort cohesion | jq -r '.summary'`

## §7 Review (pre-pr-check, code-review, task reviewers)
- Once, in the main session: `code-review-graph detect-changes --brief --base <base>` — risk score, test gaps, untested functions. Give this summary to every reviewer.
- Spec axis / test engineer: every untested function listed there that the change touched must be covered or explained.
- Standards axis: `code-review-graph large-functions --path <changed dir> --min-lines 60 | jq -r '.summary'` for functions the diff made long; `code-review-graph dead-code --file-pattern "<changed file>"` for new code nothing calls (Speculative Generality).
- SDD task review: `code-review-graph detect-changes --brief --base <task base SHA>`.
