# OpenCode

Checked on opencode 1.18.35.

- **Install:** OpenCode plugins are JS modules; skills come from skill folders ([skills](https://opencode.ai/docs/skills/)): `.opencode/skills/`, `.agents/skills/`, `.claude/skills/` in the project, or `~/.config/opencode/skills/`, `~/.agents/skills/`, `~/.claude/skills/`. Use a user folder, not a project one: links inside the project would show up in git, and dev-kit is personal (rule O1). Link each folder under `<dev-kit>/skills/` there, keeping its name (`ln -s <dev-kit>/skills/pre-pr-check ~/.config/opencode/skills/pre-pr-check`).
- **Allow the kit folder.** Reads outside the project need `external_directory`, which defaults to `ask`. In non-interactive `opencode run`, an `ask` is auto-rejected and one rejection ends the whole turn silently (no text back; seen 4 times in one `dk:init` run). Allow the kit folder and deny the rest explicitly, so the agent gets an error it can read instead of a dead turn. Add to `opencode.json` ([permissions](https://opencode.ai/docs/permissions/)):

  ```json
  { "permission": { "external_directory": { "*": "deny", "<dev-kit>/**": "allow" } } }
  ```
- **Try without installing:** in that run, `OPENCODE_CONFIG_DIR=<temp folder>` (with `skills/<name>` linked to each `<dev-kit>/skills/<name>`) plus `OPENCODE_CONFIG_CONTENT` carrying the permission block above loaded the kit without touching `~/.config/opencode`.
- **Kit folder:** OpenCode gives the agent the link path (for example `<config>/skills/init`). Run `realpath` on it first, then go two levels up. Do not search the disk for `RULES.md`: other CLIs' plugin caches (`~/.claude`, `~/.codex`, `~/.gemini`) hold dev-kit copies that may be older; in that run the agent searched there before resolving the link. `${CLAUDE_PLUGIN_ROOT}` is not replaced.
- **Skills:** no namespace; names must be unique across all skill folders.
- **Subagents:** the `task` tool with `subagent_type: general`. For `dk:security-auditor` / `dk:test-engineer`, tell it to read and follow `agents/<name>.md` in the kit folder.
