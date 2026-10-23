<!-- i18n: source=docs/en/README.md source_commit=v1.7.1 review=machine -->
[English](../en/README.md) | [Tiếng Việt](../vi/README.md) | 简体中文 | [日本語](../ja/README.md)

> 本译文可能滞后于英文版；以英文版为准：[README.md](../en/README.md)。

# dev-kit 文档

dev-kit（plugin 名称 `dk`）是一套帮助 agent 处理 kanban 卡片的 skill 集合：story、bug、重构，以及开 PR 之前的检查。Claude Code 是参考 CLI；Codex、Copilot CLI、Antigravity、OpenCode 和 omp 加载的是同一套 skill。该 kit 合并了三套现有的 skill 集合（Superpowers、Matt Pocock、agent-skills），并在发布前在单独的 lab 中做过测量。

这些文档提供英文、越南语（第 1–2 层）、简体中文和日语（第 1 层）版本。以英文为准；译文可能滞后。

> 文档版本：dev-kit **1.6.0**（2026-10-15）。1.0.0 是首个公开版本；文档中更早的版本号（0.x）是私有 lab 中的迭代版本。数字来自 dev-kit lab（私有）（主要是 Haiku 5.5，部分是 Sonnet 5.5，Claude Code 2.1.296），以及在工作中的一个私有 Angular 仓库上做的 backtest（Sonnet 5.5；有一次运行在 Codex 上）。尚未测量的内容标记为 ❓。

## 阅读顺序

| # | 文档 | 回答的问题 |
|---|---|---|
| 1 | [概览](01-overview.md) | dev-kit 是什么，解决什么问题，想法来自哪里，不做什么 |
| 2 | [架构](../en/02-architecture.md)（英文） | 目录结构，controller/part/rule 机制，artifact，配置 |
| 3 | [Skills](03-skills.md) | 每个 skill 做什么：步骤、输入、输出、停止点、示例 |
| 4 | [Rules](../en/04-rules.md)（英文） | 哪些 rule 是开启的，为什么，证据，如何添加新 rule |
| 5 | [安装与使用](05-setup-and-usage.md) | 在各个 CLI 上安装，运行 `dk:init`，日常使用，与其他 plugin 一起使用 |
| 6 | [证据](../en/06-evidence.md)（英文） | lab 测量了什么，结果，测量的局限 |
| 7 | [维护](../en/07-maintenance.md)（英文） | 从 upstream 更新，检查引用，版本管理 |
| 8 | [路线图与待决问题](../en/08-roadmap.md)（英文） | 缺少什么，将要做什么，需要决定什么 |
| 9 | [0.9.0 设计：init 与标准](../en/09-init-and-standards.md)（英文） | **等待批准的设计（draft 2）：** 合并后的 `dk:init`、按主题组织的标准、finding 质量、合规强制 |
| - | [术语表](glossary.md) | 文档中所用术语的定义 |

## 快速路径

- **想马上使用：** [05](05-setup-and-usage.md)，然后看 [03](03-skills.md) 的前半部分。
- **想了解为什么这样设计：** [01](01-overview.md)、[04](../en/04-rules.md)、[06](../en/06-evidence.md)。
- **想修改或扩展这个 kit：** [02](../en/02-architecture.md)、[07](../en/07-maintenance.md)。
