<!-- i18n: source=docs/en/glossary.md source_commit=v1.4.4 review=machine -->
[English](../en/glossary.md) | [Tiếng Việt](../vi/glossary.md) | 简体中文 | [日本語](../ja/glossary.md)

> 本译文可能滞后于英文版；以英文版为准：[glossary.md](../en/glossary.md)。

# 术语表

下列术语在文档中保留英文，不翻译：controller、part、rule、skill、subagent、harness、finding、certain / suspect、verdict、GO / NO-GO、backtest、baseline、worktree、artifact、report-only、self-review、blast radius、plugin、marketplace。

| 术语 | 在 dev-kit 中的含义 |
|---|---|
| **Controller** | 编排某一种卡片类型的 skill（`dk:story-runner`、`dk:bug-fixer`、`dk:code-refactor`、`dk:pre-pr-check`）：决定步骤、读取 part、应用 rule、写报告 |
| **Part** | 从 upstream 套件复制来的子 skill，放在 `parts/` 中，不注册为 skill；controller 在需要时读取该文件 |
| **Rule** | `rules/RULES.md` 中的一条简短指令，带有开/关状态和证据 |
| **Baseline** | 没有安装任何 skill 集合的同一个模型；lab 中用于比较的参照点 |
| **SDD**（subagent-driven development） | Superpowers 的工作方式：把 plan 拆成任务，为每个任务启动一个 subagent，再为每个任务启动一个 subagent 来 review；用一份 ledger 使运行可以恢复 |
| **Worktree** | 为某个分支准备的独立 git 工作目录，使大型工作不会触碰主目录 |
| **Grilling** | Matt Pocock 澄清需求的方式：沿着设计决策树，一次问一个问题 |
| **Characterization test** | 在重构之前固定当前行为的测试，包括看起来像 bug 的行为 |
| **Pre-PR / final gate** | 开 PR 之前的检查：运行检查命令、查找降低标准的迹象、review，并给出 GO/NO-GO verdict |
| **Lowered standard** | 为了“快速通过”而走的捷径：跳过测试、添加 `noqa`/`ts-ignore`、删除 assert、降低阈值 |
| **Artifact** | agent 留给人类读者的文件：spec、plan、报告、PR 文本，位于 `.dev-kit/` 中 |
| **Headless** | 在没有人回答的情况下运行（`claude -p`），就像在 lab 中那样 |
| **Overfit** | 根据某个具体任务写出的 rule，只对那个任务有帮助，对同类的新任务没有帮助 |
| **Upstream** | 原始的套件：Superpowers、mattpocock/skills、agent-skills |
| **Dogfood** | 在你自己的真实工作中使用 dev-kit 并记录日志 |
