English | [Tiếng Việt](../vi/07-maintenance.md)

# 7. Maintenance

## 7.1 Principles

- **`parts/` are modified copies.** Any change to a part is recorded in [`UPSTREAM.md`](../../UPSTREAM.md), so the next update knows what to re-apply.
- **Controllers and rules are written in-house** and do not depend on upstream.
- **Every behavior change** needs a line in [`CHANGELOG.md`](../../CHANGELOG.md). If it is a rule, add the evidence in `rules/RULES.md`.

## 7.2 Check references after every edit

```bash
python3 scripts/check_parts.py .
```

The script reports an error when:
- a part or controller mentions a part that does not exist (`parts/<x>/SKILL.md`, "dev-kit part \`x\`");
- a relative Markdown link is broken.

Links inside code fences (illustrative examples) are ignored.

## 7.3 Updating from upstream

1. Download the new version of the original kit into a temporary folder, next to the pinned one. The current commit is recorded in `UPSTREAM.md`.
2. `diff` the two versions, only for the parts dev-kit uses.
3. For each part that changed:
   - **"Unchanged" part** (the Edits column says "none yet"): copy over it.
   - **Part with edits:** copy over it, then re-apply the recorded edits.
   - **SDD** (the most edited): read the diff and choose what to take.
4. Run `scripts/check_parts.py`.
5. Re-run the lab (at least the sample-app cards and a few SWE tasks) and compare with the previous run. If it gets worse, do not release.
6. Update `UPSTREAM.md` (new commit), `CHANGELOG.md`, and the version with `python3 scripts/bump_version.py <x.y.z>`.

## 7.4 Adding a new part

1. Copy the whole skill folder from the original kit into `parts/<name>/`.
2. Change references of the form `<kit>:<skill>` to "dev-kit part \`<skill>\` (parts/<skill>/SKILL.md)". Copy the referenced part too, or drop the reference.
3. Add a line to `UPSTREAM.md` and the source's LICENSE (if it is a new source) to `LICENSES/`.
4. Attach the part to a controller step. Do not copy a part nobody uses.
5. Run `check_parts.py`, then measure with the lab.

## 7.5 Versioning

| Change | Version |
|---|---|
| Wording, docs, bug fixes that do not change behavior | patch (1.0.x) |
| Changing the controller flow, enabling/disabling a rule, adding a part | minor (1.x.0) |
| Renaming a skill, moving the artifact location, changing the config schema | major (x.0.0); describe the migration in the CHANGELOG |

The version lives in several manifests (Claude Code, Codex, Cursor, Antigravity), listed in `.version-bump.json`. Always change it with `python3 scripts/bump_version.py <x.y.z>`; `--check` fails when the manifests disagree. Codex, Copilot and `agy` install a copy, so after changing the kit you must reinstall; Codex stores the copy in a per-version folder (`~/.codex/plugins/cache/dev-kit/dk/<version>/`), so the version must be bumped.

## 7.6 License

All three sources are MIT. The original LICENSE files are in [`LICENSES/`](../../LICENSES/). Keep them when distributing.

## 7.7 Multi-CLI support

Follow Superpowers v7.0.0: one `skills/` set, one manifest per CLI, differences go in `harness/<cli>.md`. Do not split controller content per CLI.

- **Adding a new CLI:** add a manifest (if the CLI has a plugin format), add a line to `.version-bump.json`, write `harness/<cli>.md`, and add the CLI name to the Harness section of the 5 controllers.
- **Checking after changing a controller or when a CLI has a major release:** install the kit, then ask the agent to load `pre-pr-check` and follow only the Harness section, and to return the kit directory, the first line of `rules/RULES.md`, the note file it read, and the name of the subagent tool. It passes when all four are correct.
- **Three things not to do,** taken from ADR 0002 of mattpocock/skills and a trial on 2026-10-14:
  - putting `parts/` inside `skills/`: Codex and Cursor scan skills recursively, so parts would become skills and cost context at session start;
  - gathering files with symlinks inside the plugin: Codex drops symlinks on install;
  - declaring the Codex marketplace source as `"url": "./"`: Codex treats it as a git repo and `git clone` fails; use `"source": "local", "path": "./"`.
