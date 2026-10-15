<!-- i18n: source=docs/en/05-setup-and-usage.md source_commit=v1.3.0 review=machine -->
[English](../en/05-setup-and-usage.md) | [Tiếng Việt](../vi/05-setup-and-usage.md) | [简体中文](../zh-CN/05-setup-and-usage.md) | 日本語

> この翻訳は英語版より遅れる場合があります。正式な内容は英語版です: [05-setup-and-usage.md](../en/05-setup-and-usage.md)

# 5. セットアップと使い方

## 5.1 要件

| 項目 | 備考 |
|---|---|
| エージェント CLI | Claude Code がリファレンス CLI です（lab では 2.1.296 を使用）。Codex、Copilot CLI、Antigravity (`agy`)、OpenCode、omp も kit を読み込めます（5.2 節）。 |
| `git` | 必須 |
| リポジトリのチェックコマンド | `make check`、`npm test` など。`dk:init` が検出して記録します |
| `gh` | 任意。dev-kit 自身が PR を開くことはありません |
| `codegraph`、`code-review-graph` | 任意。`dk:init` が `scripts/install-graph-tools.sh` で確認します。足りない場合は確認したうえで、そのスクリプトでインストールし、既定でインデックスを構築します |

## 5.2 インストール

dev-kit は Superpowers の方式に従います: **1 つの `skills/` セットと、CLI ごとに 1 つの manifest**。CLI 間で異なる部分は [`harness/`](../../harness/README.md) にあります。各 controller は **Harness** の段落で始まります。`${CLAUDE_PLUGIN_ROOT}` を置換しない CLI では、エージェントが kit ディレクトリを自分で見つけ（symlink を解決したうえで `SKILL.md` の 2 つ上）、その CLI 向けの注意事項を読みます。

**Claude Code**（リファレンス CLI）:

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

セッション内では、`/plugin marketplace add awesome-boilerplate-develop/dev-kit` のあと `/plugin install dk@dev-kit` を実行します。インストールせずにローカルのチェックアウトを試すには（たとえば kit を変更している間）: `claude --plugin-dir /path/to/dev-kit`。

読み込まれたかの確認: セッション内で、エージェントに `dk:` で始まる skill を一覧させます。5 つすべてが見えるはずです: `dk:init`、`dk:story-runner`、`dk:bug-fixer`、`dk:code-refactor`、`dk:pre-pr-check`。

**その他の CLI**（2026-10-14 に公開リポジトリからインストールして確認。詳細と注意点は `harness/` の各ファイルにあります）:

| CLI | インストールコマンド | 備考 |
|---|---|---|
| Codex 0.160.1 | `codex plugin marketplace add awesome-boilerplate-develop/dev-kit` のあと `codex plugin add dk@dev-kit` | Codex はバージョンごとにコピーをインストールします（[codex.md](../../harness/codex.md)） |
| Copilot CLI 1.0.89 | `copilot plugin marketplace add awesome-boilerplate-develop/dev-kit` のあと `copilot plugin install dk@dev-kit` | リポジトリやパスから直接インストールする方法も動作しますが、非推奨と報告されています（[copilot.md](../../harness/copilot.md)） |
| Antigravity 1.3.5 | `agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit` | `agy` は `agents/` と `rules/*.md` の両方を登録します（[antigravity.md](../../harness/antigravity.md)） |
| omp 18.10.4 | `omp plugin marketplace add awesome-boilerplate-develop/dev-kit` のあと `omp plugin install dk@dev-kit` | omp は Claude Code plugin を読み込みます。2 つのレビューエージェントは名前付きの task エージェントとして現れます（[omp.md](../../harness/omp.md)） |
| OpenCode 1.18.35 | リポジトリを clone し、各 `skills/<name>` ディレクトリを `~/.config/opencode/skills/` にリンクする | `permission.external_directory` で kit ディレクトリの読み取りを許可してください（[opencode.md](../../harness/opencode.md)） |

非対応:
- **Gemini CLI:** 2026-06-18 以降、Google は無料枠と Google One のユーザーを Antigravity CLI に移行しました。
- **Cursor（1.2.3 で削除）:** `cursor-agent` にログインが必要なため、一度も検証できませんでした。
- **pi（現時点では見送り）:** pi 1.0.2 は kit をインストールして読み込みますが、pi のコアには subagent ツールがないため、すべてのレビューの役割をメインセッションで実行することになります。このモードは測定していません。

dev-kit の rule と lab の根拠は Claude で測定したものです。表の CLI では、kit が読み込まれることは確認済みです。レビュー品質は Codex での 1 回の backtest だけで、他の CLI は未測定です（[06](../en/06-evidence.md)、英語）。

## 5.3 すべてのプロジェクトにインストールするか、プロジェクトごとにインストールするか

| 方法 | 範囲 | 備考 |
|---|---|---|
| `claude --plugin-dir /path/to/dev-kit` | そのセッションのみ | ローカルのチェックアウトを読み込みます。設定には触れません。kit を変更している間に便利です |
| `claude plugin install dk@dev-kit` | 既定ではユーザー（全プロジェクト） | インストール結果は `scope: user` と報告されました（2026-10-14）。プロジェクト限定のオプションは未検証です ❓ |

おすすめ: ユーザー向けにインストールし、`dk:init` は実際に使うリポジトリでだけ実行してください。リポジトリで共有される `.claude/settings.json` では dev-kit を有効にしないでください。これは個人用の kit です（rule O1）。

## 5.4 他の plugin（Superpowers、code-review…）との併用

**名前の衝突はありません:**
- plugin の skill には必ず plugin 名が接頭辞として付きます（`superpowers:…`、`code-review:…`、`dk:…`）。
- dev-kit のサブ skill は `parts/` にあり、skill としては登録されません。

**他の plugin をオフにする必要はありません。** lab では、実際のグローバル設定（Superpowers と公式の `code-review` を含む 17 個の plugin）で 3 枚のカード（B1、S1、P2）を実行しました。
- **呼び出されたのは `dk:*` skill だけで**、品質は保たれました（欠陥 3/3、8/8、5/5）。
- **コストは単独の場合より約 15–50% 高く**なりました。有効な plugin ごとに、skill の説明と hook がコンテキストに加わるためです。

**知っておくと良いこと:**
- **そのテストでは skill を名前で呼び出しました**（`Use skill dk:…`）。「このバグを直して」のように一般的にしか言わないと、`SessionStart` hook（`using-superpowers`）によって Superpowers が skill の選択を取ることがあります。未測定です ❓。controller を名前で呼び出すのが安全な方法です。
- **コンテキストを節約するには**、そのプロジェクトで必要な plugin だけを有効にしてください。

## 5.5 スクリプトでグラフツールをインストールする

```bash
bash /path/to/dev-kit/scripts/install-graph-tools.sh --check    # see what is already installed
bash /path/to/dev-kit/scripts/install-graph-tools.sh --install  # install the pinned version of whatever is missing
```

| ツール | 固定バージョン | インストール方法 |
|---|---|---|
| codegraph | v1.5.0 | codegraph 公式の `install.sh`（タグで固定）。`~/.codegraph/` と `~/.local/bin/codegraph` に配置される |
| code-review-graph | 2.3.9 | `pipx`。pipx がなければ `uv tool` にフォールバックする |

**注意:**
- **すでにインストールされているツールはそのままです。** スクリプトはアップグレードもダウングレードもしません。codegraph の `install.sh` はインストール時に他のバージョンを削除するためです。
- **スクリプトは MCP サーバーも hook も登録しません**（`… install` を実行することはありません）。
- **`dk:init` は、あなたに確認したうえでこのスクリプトを呼び出します。** 自分で実行することもできます。

## 5.6 グラフツールをインストールしない場合

**実行には影響しません:** どの controller も、すべてのステップをそのまま行います。off になるのは rule G1 だけです。
- エージェントは `codegraph` ではなく、grep とファイル読み取りでコードを探します。
- `pre-pr-check` には、リスクとテスト不足についての CRG の要約がありません。

lab では SWE の Django タスク 17 件（Haiku）を測定しました。インデックスがある場合もない場合も 10/17 を解決し、コストは同じでした。変わったのは、エージェントが grep を使う頻度が約半分になったことだけです。コードを見つけること自体が難しい、大きなリポジトリや不慣れなリポジトリでは、効果がもっとはっきり出るかもしれません。これは未測定です ❓。

## 5.7 リポジトリでの初回

```text
Use skill dk:init for this repo.
```

エージェントはまずリポジトリを調べ、そのあと質問を 1 つずつ順番に行います: コマンドとベースブランチ、グラフのインデックス、baseline（red の場合のみ）、トピックごとの standards チェックリスト（コードから提案される rule つき）、その他の規約についての自由質問 1 つ、そして任意の `CONSTRAINTS.md` です。各質問には根拠と既定値が示されます。「default」「skip」またはあなたの答えを返してください。`.dev-kit/`（git に無視され、コミットするものはありません）を作成します。あとで 1 つの部分だけやり直すには: `dk:init index`、`dk:init baseline`、`dk:init standards [topic]`。

## 5.8 日常の使い方

カードの種類に応じて controller を呼び出し、カードを貼り付けます。

```text
Use skill dk:bug-fixer for this card:
<card text / issue link>
```

| カードの種類 | Skill |
|---|---|
| 機能/ストーリー | `dk:story-runner` |
| バグ、パフォーマンスの問題 | `dk:bug-fixer` |
| 技術的負債、リファクタリング | `dk:code-refactor` |
| 完成したブランチ、PR 前のチェック | `dk:pre-pr-check` |
| 他の人のブランチを変更せずにチェックする | `dk:pre-pr-check`。「report only, do not change code」と言い添える |

**既定より深いレビューが必要なとき:** 「review with all 4 reviewers」とはっきり言ってください（rule C2）。

**確認する出力:**
- `.dev-kit/reports/<name>.md`: 何を行ったか、なぜか、実行したコマンドとその結果。
- `.dev-kit/reports/pr-body.md`: 下書きの PR 本文。
- `.dev-kit/specs/`（story）: 特に **Decisions** セクションで、エージェントが何を決めたかを確認する。
- 現在のブランチ上のコミット。dev-kit は push せず、PR も開きません。

## 5.9 試用ログをつける

カードごとに、[`templates/dogfood-log.md`](../../templates/dogfood-log.md) のコピーに 1 行ずつ書きます。
- たどった経路（直接か SDD か、レビューの深さ）。
- やり直しが必要だったか。
- レビューが実際に何を捕捉したか。
- コスト。
- プロセスが邪魔になったか。

週末に、テンプレートの末尾にある 4 つの質問に答えてください。lab では「実際の人にとって役に立つか」を測定できないため、これが次の一手を決めるための主なデータになります。

## 5.10 うまくいかないとき

| 症状 | 確認すること |
|---|---|
| `dk:*` skill が表示されない | plugin は読み込まれているか（`--plugin-dir` または `/plugin`）。パスは正しいか |
| エージェントが controller に従わず `superpowers:…` を呼び出す | `dk:<controller>` を名前で呼び出す。それでも先取りされるなら、そのプロジェクトで Superpowers をオフにする（5.4） |
| controller が途中で止まる | transcript を添えて報告する。rule F1 があれば防げたはず |
| 普通の diff なのに 4 人のレビュアーが動く | diff が auth/シークレット/個人データ/config/マイグレーションに触れていないか確認する。触れていなければ、rule C2 の適用のバグ |
| レポートにチェックコマンドの出力がない | `.dev-kit/config.yml` のコマンドが間違っているか、ない: `dk:init` を再実行する |
