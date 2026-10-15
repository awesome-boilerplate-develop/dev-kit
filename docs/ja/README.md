<!-- i18n: source=docs/en/README.md source_commit=v1.4.10 review=machine -->
[English](../en/README.md) | [Tiếng Việt](../vi/README.md) | [简体中文](../zh-CN/README.md) | 日本語

> この翻訳は英語版より遅れる場合があります。正式な内容は英語版です: [README.md](../en/README.md)

# dev-kit ドキュメント

dev-kit（plugin 名 `dk`）は、エージェントがかんばんカード（ストーリー、バグ、リファクタリング、PR を開く前のチェック）を進めるのを助ける skill セットです。Claude Code がリファレンス CLI で、Codex、Copilot CLI、Antigravity、OpenCode、omp でも同じ skill セットを読み込めます。この kit は既存の 3 つのセット（Superpowers、Matt Pocock、agent-skills）を統合したもので、リリース前に別の lab で測定されました。

これらのドキュメントは、英語、ベトナム語（tier 1–2）、簡体字中国語と日本語（tier 1）で提供されています。正式な内容は英語版で、翻訳は遅れる場合があります。日本語版にないドキュメントは英語版へのリンクで、表の「言語」列に「英語」と示しています。

> ドキュメントのバージョン: dev-kit **1.4.10**（2026-10-15）。1.0.0 が最初の公開リリースでした。ドキュメント内のそれ以前のバージョン番号（0.x）は非公開の lab での反復版です。数値は dev-kit の lab（非公開）（主に Haiku 5.5、一部 Sonnet 5.5、Claude Code 2.1.296）と、職場の非公開 Angular リポジトリでの backtest（Sonnet 5.5。Codex での実行が 1 回）によるものです。まだ測定していないものには ❓ を付けています。

## 読む順番

| # | ドキュメント | 言語 | 答える内容 |
|---|---|---|---|
| 1 | [概要](01-overview.md) | 日本語 | dev-kit とは何か、どんな問題を解決するか、アイデアの出どころ、何をしないか |
| 2 | [Architecture](../en/02-architecture.md) | 英語 | ディレクトリ構成、controller/part/rule の仕組み、artifact、設定 |
| 3 | [Skills](03-skills.md) | 日本語 | 各 skill の動作: ステップ、入力、出力、停止点、例 |
| 4 | [Rules](../en/04-rules.md) | 英語 | どの rule が on か、その理由、根拠、新しい rule の追加方法 |
| 5 | [セットアップと使い方](05-setup-and-usage.md) | 日本語 | 各 CLI へのインストール、`dk:init` の実行、日常の使い方、他の plugin との併用 |
| 6 | [Evidence](../en/06-evidence.md) | 英語 | lab が測定したこと、結果、測定の限界 |
| 7 | [Maintenance](../en/07-maintenance.md) | 英語 | upstream からの更新、参照のチェック、バージョン管理 |
| 8 | [Roadmap and open questions](../en/08-roadmap.md) | 英語 | 不足していること、今後行うこと、決める必要があること |
| 9 | [0.9.0 design: init and standards](../en/09-init-and-standards.md) | 英語 | **承認待ちの設計（ドラフト 2）:** 統合された `dk:init`、トピック別の standards、finding の品質、遵守の強制 |
| - | [用語集](glossary.md) | 日本語 | ドキュメントで使う用語の定義 |

## クイックパス

- **今すぐ使いたい:** [05](05-setup-and-usage.md)、続いて [03](03-skills.md) の前半。
- **なぜこの設計なのかを理解したい:** [01](01-overview.md)、[04](../en/04-rules.md)、[06](../en/06-evidence.md)。
- **kit を変更または拡張したい:** [02](../en/02-architecture.md)、[07](../en/07-maintenance.md)。
