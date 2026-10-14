# Antigravity (`agy`)

Checked on agy 1.3.5.

- **Install:** `agy plugin install <path or repo>` (reads `.antigravity-plugin/plugin.json`); `agy plugin validate <path>` lists what it will load. Reinstall after changing the kit: agy installs a copy.
- **Kit folder:** the installed copy, `~/.gemini/config/plugins/dk/`; agy copies the whole tree. `${CLAUDE_PLUGIN_ROOT}` is not replaced. In one smoke run after a local install, the agent resolved the source folder instead of the copy; both held the same files, but after editing the kit, reinstall so the two stay equal.
- **Components agy registers:** `skills/`, `agents/` (as agents) and `rules/*.md` (as plugin rules). In one probe the text of a registered rule was not in the model's context; dev-kit's `rules/` are read on demand by the controllers either way.
- **Subagents:** the `invoke_subagent` tool. For `dk:security-auditor` / `dk:test-engineer`, tell the subagent to read and follow `agents/<name>.md` in the kit folder.
