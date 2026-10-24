<!-- i18n: source=docs/en/01-overview.md source_commit=v1.7.5 review=machine -->
[English](../en/01-overview.md) | [Tiếng Việt](../vi/01-overview.md) | [简体中文](../zh-CN/01-overview.md) | 日本語

> この翻訳は英語版より遅れる場合があります。正式な内容は英語版です: [01-overview.md](../en/01-overview.md)

# 1. 概要

## 1.1 dev-kit とは

dev-kit は **5 つの skill** を持つ Claude Code plugin です。

| Skill | 役割 |
|---|---|
| `dk:init` | マシンとリポジトリの環境を整える |
| `dk:story-runner` | ストーリー/機能カードを最初から最後まで進める |
| `dk:bug-fixer` | バグカードを修正し、再発を防ぐテストを付ける |
| `dk:code-refactor` | 振る舞いを変えずに再構成する |
| `dk:pre-pr-check` | PR を開く前の最終チェック |

後ろの 4 つが **controller** です。自分でステップを選び、必要に応じて「part」（サブ skill）を呼び出すオーケストレーション用の skill です。この kit には、レビュー用のエージェントペルソナも 2 つあります: `dk:security-auditor` と `dk:test-engineer` です。

## 1.2 問題

毎日エージェントと作業していると、3 つの問題が繰り返し起こります。

1. **毎回スタイルが違う。** 同じ種類のカードでも、エージェントがテストを先に書くときと書かないとき、レポートを出すときと出さないときがあります。読み手がチェックしにくくなります。
2. **複数の skill セットを入れると衝突する。** Superpowers、Matt Pocock、agent-skills... それぞれ得意な分野があります。一緒にインストールすると次のようになります。
   - skill 名が衝突する（たとえば `test-driven-development` が 2 つある）。
   - あるセットの bootstrap が、skill の選択の主導権をめぐって別のセットと争う。
   - 「ユーザー呼び出し専用」の skill が多く、自動のフローが止まる。
3. **どのセットが本当に役立つのか分からない。** 各セットは多くを約束しますが、自分たちの作業で測定した人はいません。

## 1.3 考え方

1. **カードの種類ごとに controller を置く:** 作業の種類ごとにオーケストレーション用の skill を 1 つ用意し、適切なステップで適切なサブ skill を呼び出します。
2. **コピーして 1 つのセットに統合する:** 元の plugin はインストールしません。必要な部分をコピーし、名前と参照を直し、出どころを記録します。内容はすべて自分たちのものなので、衝突は起こりません。
3. **根拠のあるものだけを残す:** すべての選択（どのステップを実行するか、レビュアーは何人か、どの rule を on にするか）は、まず lab で測定します。コストがかかるのに役立たないものは、既定のパスから外します。

## 1.4 どのセットから何を取ったか

| ソース | 取り入れたもの | 用途 |
|---|---|---|
| Superpowers v6.4.2 | planning、worktree、subagent-driven development (SDD)、TDD、systematic debugging、「完了」と言う前の検証、レビューの受け取り、ブランチの終了処理 | 大きな作業の実行、デバッグ |
| mattpocock/skills v1.3.1 | grilling（確認のための質問）、domain-modeling、codebase-design、2 軸の code-review、pr、diagnosing-bugs | 要件の明確化、モジュール設計、レビュー、PR の文面、パフォーマンスのバグ |
| agent-skills 0.6.12 | constraint-driven-development、ペルソナ `security-auditor` と `test-engineer` | 基準の引き下げを防ぐ、セキュリティとテストのレビュー |

ソース、コミット、変更点の詳細: [`UPSTREAM.md`](../../UPSTREAM.md)。

## 1.5 測定結果のまとめ

lab より（詳細は [06](../en/06-evidence.md)、英語）:
- **品質:** controller なしでモデルに単独で作業させた場合と同等です。サンプルアプリのカードと、SWE-bench Verified (Django) のタスク 13 件で測定しました。
- **コスト:** モデルに単独で作業させた場合の約 **2 倍**です。最初のバージョン（重いものをすべて統合したもの）では 3–13 倍かかったこともありました。
- **価値があるのは:**
  - 一貫したレポートと、読み手のための artifact。
  - 最終レビュー層。
  - 根拠のある短い rule セット。
  - セット間の衝突がないこと。

  重いオーケストレーション（SDD、多数のレビュアー）は、lab ではコードをより正しくは**しません**でした。

## 1.6 dev-kit がしないこと

- コードを push したり、PR を開いたりはしません。結果は現在のブランチ上のコミットと、用意された PR の文面です。
- 要件についてのあなたの判断を肩代わりしません。カードが曖昧なときは skill があなたに質問します。人がいない状態（headless）で実行しているときだけ、自分で選び、その選択を前提（assumption）として記録します。
- 確認なしにツールをインストールしたり、リポジトリの外の設定を変更したりしません。
- まだトラッカー（GitHub Issues、Jira...）やコードグラフツール（codegraph、code-review-graph）とは連携していません。[08](../en/08-roadmap.md)（英語）を参照してください。
