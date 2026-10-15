<!-- i18n: source=docs/en/glossary.md source_commit=v1.4.2 review=machine -->
[English](../en/glossary.md) | [Tiếng Việt](../vi/glossary.md) | [简体中文](../zh-CN/glossary.md) | 日本語

> この翻訳は英語版より遅れる場合があります。正式な内容は英語版です: [glossary.md](../en/glossary.md)

# 用語集

次の用語は英語のまま使います: controller、part、rule、skill、subagent、harness、finding、certain / suspect（tier）、verdict、GO / NO-GO、backtest、baseline、worktree、artifact、report-only、self-review、blast radius、plugin、marketplace。それ以外の用語は下の表に従います。

| 用語 | dev-kit での意味 |
|---|---|
| **Controller** | 1 種類のカードをオーケストレーションする skill（`dk:story-runner`、`dk:bug-fixer`、`dk:code-refactor`、`dk:pre-pr-check`）: ステップを決め、part を読み、rule を適用し、レポートを書く |
| **Part** | upstream のセットからコピーして `parts/` に置いたサブ skill。skill としては登録されず、controller が必要なときにファイルを読む |
| **Rule** | `rules/RULES.md` にある短い指示。on/off の状態と根拠を持つ |
| **Baseline** | skill セットをインストールしていない同じモデル。lab での比較の基準点 |
| **SDD** (subagent-driven development) | Superpowers の作業方法: 計画をタスクに分割し、タスクごとに subagent を起動し、各タスクをレビューする subagent も起動する。台帳により実行を再開できる |
| **Worktree** | ブランチ用の別個の git 作業ディレクトリ。大きな作業がメインのディレクトリに影響しないようにする |
| **Grilling** | Matt Pocock の要件の明確化の方法: 設計判断のツリーをたどりながら、一度に 1 つずつ質問する |
| **Characterization test** | リファクタリングの前に現在の振る舞いを固定するテスト。バグに見える振る舞いも含む |
| **Pre-PR / final gate** | PR を開く前のチェック: チェックを実行し、基準引き下げの兆候を探し、レビューして、GO/NO-GO の verdict を出す |
| **Lowered standard（基準の引き下げ）** | 「手早く通す」ための近道: テストのスキップ、`noqa`/`ts-ignore` の追加、assert の削除、しきい値の引き下げ |
| **Artifact** | エージェントが人間の読み手のために残すファイル: spec、plan、レポート、PR の文面。`.dev-kit/` に置かれる |
| **Headless** | 答える人間がいない状態での実行（`claude -p`）。lab ではこの方法だった |
| **Overfit** | 特定の 1 つのタスクから書かれた rule が、そのタスクにしか効かず、同じ種類の新しいタスクには効かないこと |
| **Upstream** | 元のセット: Superpowers、mattpocock/skills、agent-skills |
| **Dogfood** | 自分の実際の作業で dev-kit を使い、ログを残すこと |
