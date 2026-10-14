# omp

Checked on omp 18.10.4.

- **Install:** omp reads Claude Code plugins. Try with `omp --plugin-dir <dev-kit>`; install with `omp plugin marketplace add <dev-kit or owner/repo>` (omp reads `.claude-plugin/marketplace.json` when `.omp-plugin/marketplace.json` is absent) and `omp plugin install dk@dev-kit`. Docs: `omp://marketplace.md`.
- **Kit folder:** the plugin root (with `--plugin-dir`, the folder you passed). `${CLAUDE_PLUGIN_ROOT}` is not replaced in `SKILL.md`; omp gives the agent the skill's `SKILL.md` path, so "two levels above" works.
- **Skills:** one level under `skills/` only, so `parts/` are not registered (`omp://skills.md`). A skill can also be read as `skill://<name>`; a same-named skill from another source gets a `<namespace>/<name>` alias.
- **Subagents:** the `task` tool. omp also discovers `agents/*.md` of Claude-format plugins as task agents when the `claude-plugins` provider is enabled (`omp://task-agent-discovery.md`); with `--plugin-dir`, `security-auditor` and `test-engineer` were offered as named agents in a 2026-10-14 smoke run. If they are not offered, give a `task` subagent the instruction to read and follow `agents/<name>.md` in the kit folder.
