# Codex

Checked on codex-cli 0.160.1.

- **Install:** `codex plugin marketplace add <dev-kit path or owner/repo>` (reads `.agents/plugins/marketplace.json`, marketplace `dev-kit`), then `codex plugin add dk@dev-kit`. After changing the kit, bump the version and run `codex plugin add` again: Codex installs a copy.
- **Kit folder:** the installed copy, `~/.codex/plugins/cache/dev-kit/dk/<version>/`. Codex copies the whole tree (parts, rules, templates, scripts, standards, agents) and lists each skill with its `SKILL.md` path, so "two levels above this SKILL.md" resolves there. `${CLAUDE_PLUGIN_ROOT}` is not replaced.
- **Skills:** found under `skills/` only (`.codex-plugin/plugin.json` → `"skills": "./skills/"`); `parts/` are not registered. Mention a skill explicitly with `$<skill>`.
- **Subagents:** the spawn tool (`spawn_agent`, shown as `collaboration.spawn_agent`). Current releases enable subagents by default and spawn them when skill instructions ask. A subagent inherits the parent's model, reasoning effort and sandbox unless the spawn sets them ([Codex subagents](https://developers.openai.com/codex/subagents)).
  - Give reviewers a fresh context. Superpowers v7.0.0 (`skills/using-superpowers/references/codex-tools.md`) notes that `spawn_agent {fork_turns: "none"}` gives a clean child while the default copies the transcript; not measured in dev-kit.
  - `dk:security-auditor`, `dk:test-engineer`: spawn a subagent told to read and follow `agents/<name>.md` in the kit folder. Codex custom agents are TOML files under `~/.codex/agents/`; dev-kit does not install them.
  - Checking a run: `codex exec --json` does not emit `spawn_agent` calls (only `wait` items). The full record is the session rollout, `~/.codex/sessions/<yyyy>/<mm>/<dd>/rollout-*.jsonl`, one file per subagent. In the 2026-10-14 backtest of `pre-pr-check` (four-reviewer depth), the rollout shows four `spawn_agent` calls with `fork_turns: "none"` (standards, spec, security, tests).
