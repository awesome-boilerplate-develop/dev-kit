<!-- i18n: source=README.md source_commit=v1.2.0 review=machine -->
[English](README.md) | [Tiếng Việt](README.vi.md) | [简体中文](README.zh-CN.md) | 日本語

> この翻訳は英語版より遅れる場合があります。正式な内容は英語版です: [README.md](README.md)

# dev-kit

[![Release](https://img.shields.io/github/v/release/awesome-boilerplate-develop/dev-kit)](https://github.com/awesome-boilerplate-develop/dev-kit/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![docs](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml/badge.svg)](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml)

かんばんカードの作業（ストーリー、バグ、リファクタリング、PR を開く前のチェック）のための agent skill セットです。skill が従う rule は、測定した lab で効果があったものだけを残しています。

**Claude Code**（リファレンス）、**Codex**、**GitHub Copilot CLI**、**Antigravity**、**OpenCode**、**omp** で動作します。

## Skills

| Skill | 使う場面 |
|---|---|
| `dk:init` | リポジトリでの初回: ツールを確認し、`.dev-kit/config.yml` を書き、テストの baseline を記録する |
| `dk:story-runner` | 機能/ストーリーのカード: 確認、spec、テスト付きの実装、そのあと `dk:pre-pr-check` |
| `dk:bug-fixer` | バグのカード（パフォーマンスの回帰を含む）: 根本原因、回帰テスト、修正 |
| `dk:code-refactor` | 技術的負債のカード: 振る舞いを変えずに再構成する |
| `dk:pre-pr-check` | 完成したブランチ: チェックを実行し、リスクに応じた深さでレビューし、レポートと PR の文面を書く |

plugin 名は `dk` です。CLI によっては skill が `dk:` 接頭辞なしで表示されます。

## インストール

### Claude Code

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

セッション内では、`/plugin marketplace add awesome-boilerplate-develop/dev-kit` と `/plugin install dk@dev-kit` で同じことができます。

### Codex

```bash
codex plugin marketplace add awesome-boilerplate-develop/dev-kit
codex plugin add dk@dev-kit
```

### GitHub Copilot CLI

```bash
copilot plugin marketplace add awesome-boilerplate-develop/dev-kit
copilot plugin install dk@dev-kit
```

### Antigravity

```bash
agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit
```

### omp

```bash
omp plugin marketplace add awesome-boilerplate-develop/dev-kit
omp plugin install dk@dev-kit
```

### OpenCode

OpenCode は skill をフォルダから読み込むため、リポジトリを clone して skill をユーザーの skill フォルダにリンクします:

```bash
git clone https://github.com/awesome-boilerplate-develop/dev-kit ~/dev-kit
mkdir -p ~/.config/opencode/skills
for s in ~/dev-kit/skills/*; do ln -s "$s" ~/.config/opencode/skills/; done
```

そのあと、`~/.config/opencode/opencode.json` で OpenCode に kit フォルダの読み取りを許可します:

```json
{ "permission": { "external_directory": { "~/dev-kit/**": "allow" } } }
```

### その他の CLI

- **Cursor:** manifest は含まれていますが、まだ検証していません。
- **非対応:** Gemini CLI（Google は無料枠のユーザーを Antigravity に移行しました）、pi（pi のコアに subagent ツールがありません）。

CLI ごとの詳細（インストール先、subagent ツール、既知の注意点）: [`harness/`](harness/README.md)。

## クイックスタート

1. エージェントでリポジトリを開き、**`dk:init` を使う**よう頼みます。まずリポジトリを調べ、そのあと少数の質問を 1 つずつ行い（コマンド、グラフのインデックス、トピックごとの standards チェックリストとコードから提案される rule）、`.dev-kit/` を作成して、現在のテストの baseline を記録します。
2. カードを名前で渡します:

   ```text
   Use dk:bug-fixer for this card: "Checkout total drops to 0 when two promotions apply."
   ```

3. 終わると、コミット、`.dev-kit/reports/` の短いレポート、そして `dk:pre-pr-check` による GO / NO-GO の verdict が得られます。

## 仕組み

- **薄い controller。** 各 controller は、セッション内で直接作業する短い skill です。controller が借りる長めの playbook（TDD、デバッグ、計画、レビューなど）は `parts/` にあり、ステップで必要になったときだけ読み込まれるため、セッション開始時にコンテキストを消費しません。
- **根拠のある rule。** [`rules/RULES.md`](rules/RULES.md) に各 rule、その on/off の状態、根拠となる lab の結果を載せています。rule は、未知のタスク 5 件以上で効果があった場合にだけ on にします。
- **リスクに応じたレビューの深さ。** `dk:pre-pr-check` は、diff の大きさと種類から、self-review、レビュアー 1 人、または 4 人（standards、spec、セキュリティ、テスト）のいずれかを選びます。
- **機械でチェックするレポート。** [`scripts/check_report.py`](scripts/check_report.py) は、"certain" の finding が変更されたコード内にあり、一般的な「テスト不足」の指摘ではなく、存在する rule だけを引用するまで、レポートを受け付けません。
- **個人用で、push されない。** dev-kit が書くもの（config、specs、plans、reports、あなたのプロジェクトの standards）はすべて `.dev-kit/` に置かれ、このフォルダは git から自分自身を無視します。dev-kit は `.gitignore`、`CLAUDE.md`、`AGENTS.md` など、追跡されているファイルを一切編集しません。
- **階層化された standards。** kit の standards、好きな方法で共有できるチーム用フォルダ（`standards.team`）、`.dev-kit/standards/` にあなた自身のプロジェクトの standards。各レビュアーは自分の役割に合うトピックだけを受け取ります。
- **グラフツール（任意）。** [codegraph](https://github.com/colbymchenry/codegraph) と code-review-graph のインデックスがあれば、controller はコードを探し、blast radius を測り、レビュー前に `detect-changes` を実行します。

## 測定したこと

- **Lab**（234 回の実行、Haiku 5.5、サンプルアプリと SWE-bench Verified の Django タスク 13 件）: コード品質はモデルに単独で作業させた場合と同等で、コストは約 2 倍です。追加のコストはレビュー層と artifact に使われ、コードがより正しくなるわけではありません。
- **実際のバグに対する backtest**（非公開の Angular リポジトリ、Sonnet 5.5）: レビューのステップを強制すると、`detect-changes` の利用が 2/6 から 6/6 の PR に増えました。実際のバグを捕捉できるかは、実行ごとに大きくばらつきます。
- **社内 UI コントロールのプロジェクト rule** がエージェントの書くコードを変えました（rule があると社内タグ 6 件と 10 件、rule がないと Material タグ 18 件と 16 件）: エージェントが自力では知り得ない知識なので、最も明確な成果です。

詳細と限界: [docs/en/06-evidence.md](docs/en/06-evidence.md)。

## ドキュメント

- [ドキュメント索引](docs/ja/README.md): 概要、アーキテクチャ、各 skill、rule、セットアップと日常の使い方、根拠、メンテナンス。
- [セットアップと使い方](docs/ja/05-setup-and-usage.md) · [Skills](docs/ja/03-skills.md) · [用語集](docs/ja/glossary.md)
- 翻訳: ベトナム語、簡体字中国語、日本語（先頭の言語リンクを参照）。英語版が正式です。

## コントリビュート

[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください: 実行するチェック、バージョニング、ドキュメントの翻訳方法。変更は [CHANGELOG.md](CHANGELOG.md) に記載しています。

## ライセンス

MIT。[LICENSE](LICENSE) を参照してください。[Superpowers](https://github.com/obra/superpowers)、[mattpocock/skills](https://github.com/mattpocock/skills)、[agent-skills](https://github.com/addyosmani/agent-skills) からコピーした部分は、それぞれの MIT ライセンスを [`LICENSES/`](LICENSES/) に保持しています。[UPSTREAM.md](UPSTREAM.md) も参照してください。
