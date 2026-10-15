English | [Tiếng Việt](../vi/README.md) | [简体中文](../zh-CN/README.md) | [日本語](../ja/README.md)

# dev-kit documentation

dev-kit (plugin name `dk`) is a skill set that helps agents work kanban cards: stories, bugs, refactors, and a check before opening a PR. Claude Code is the reference CLI; Codex, Copilot CLI, Antigravity, OpenCode and omp load the same skill set. The kit merges three existing sets (Superpowers, Matt Pocock, agent-skills) and was measured in a separate lab before release.

These docs exist in English, Vietnamese (tiers 1–2), Simplified Chinese and Japanese (tier 1). English is authoritative; translations may lag behind.

> Documentation version: dev-kit **1.4.4** (2026-10-15). 1.0.0 was the first public release; earlier version numbers in these docs (0.x) are private lab iterations. The numbers come from the dev-kit lab (private) (mostly Haiku 5.5, partly Sonnet 5.5, Claude Code 2.1.296) and from backtests on a private Angular repository at work (Sonnet 5.5; one run on Codex). Anything not yet measured is marked ❓.

## Reading order

| # | Document | Answers |
|---|---|---|
| 1 | [Overview](01-overview.md) | What dev-kit is, what problem it solves, where the ideas come from, what it does not do |
| 2 | [Architecture](02-architecture.md) | Directory layout, the controller/part/rule mechanism, artifacts, configuration |
| 3 | [Skills](03-skills.md) | What each skill does: steps, inputs, outputs, stop points, examples |
| 4 | [Rules](04-rules.md) | Which rules are on, why, the evidence, how to add a new rule |
| 5 | [Setup and usage](05-setup-and-usage.md) | Install on each CLI, run `dk:init`, daily use, use alongside other plugins |
| 6 | [Evidence](06-evidence.md) | What the lab measured, the results, the limits of the measurements |
| 7 | [Maintenance](07-maintenance.md) | Updating from upstream, checking references, versioning |
| 8 | [Roadmap and open questions](08-roadmap.md) | What is missing, what will be done, what needs deciding |
| 9 | [0.9.0 design: init and standards](09-init-and-standards.md) | **Design awaiting approval (draft 2):** merged `dk:init`, topic-based standards, finding quality, compliance enforcement |
| - | [Glossary](glossary.md) | Definitions of the terms used in the docs |

## Quick paths

- **Want to use it now:** [05](05-setup-and-usage.md), then the first part of [03](03-skills.md).
- **Want to understand why it is designed this way:** [01](01-overview.md), [04](04-rules.md), [06](06-evidence.md).
- **Want to change or extend the kit:** [02](02-architecture.md), [07](07-maintenance.md).
