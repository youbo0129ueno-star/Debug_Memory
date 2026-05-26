# Debug Memory

Debug Memory は、ソフトウェア開発中に遭遇したエラー事例を Markdown ファイルとしてローカルに蓄積し、入力したエラーメッセージに似た過去事例と解決候補を検索する CLI ツールです。Vol.1 は外部サービスに依存せず、再現可能なルールベースの検索によって、過去の記録を根拠付きで再利用できるようにします。

## Vol.1 でできること

- Markdown 形式で保存されたトラブルシューティング事例の読み込み
- エラー文や問い合わせ文から検索用シグネチャの抽出
- キーワード、タグなどに基づく類似エラー事例のランキング表示
- 一致理由、スコア、参照ファイルを含む検索結果の表示
- 解決済みの類似事例に基づく、断定を避けた解決候補の提示
- `search` と `ask` のローカル CLI コマンドの実行

## Vol.1 でやらないこと

- LLM を使った推論、回答生成、要約
- Web UI の提供
- ベクトルデータベースや埋め込み検索の導入
- 外部 API やクラウドサービスへの接続

## セットアップ

Python の仮想環境を作成し、プロジェクトを editable install します。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Windows PowerShell の場合は、仮想環境の有効化に次のコマンドを使用します。

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## 使い方

`search` は `memory/errors` 内の過去事例から類似するエラーを検索し、根拠とともにランキング表示します。

```bash
python -m debug_memory search --text "ModuleNotFoundError: No module named 'dotenv'" --top-k 3
```

出力例:

```text
Search Results
==============

[1] Pythonでdotenvが読み込めない
    score: 1.000
    status: resolved
    tags: python, dotenv, venv
    reasons:
    - ...
```

`ask` は類似事例から解決済みの候補を選び、元になった事例を証拠として添えて提示します。過去事例に基づく候補であり、現在の問題への確実な解決を保証するものではありません。

```bash
python -m debug_memory ask --text "ModuleNotFoundError: No module named 'dotenv'"
```

出力例:

```text
Debug Memory Answer
===================

Top solution candidate:
Pythonでdotenvが読み込めない

Solution:
pip install python-dotenv

Evidence:
[1] Pythonでdotenvが読み込めない
    status: resolved
```

既定以外の事例ディレクトリを検索する場合は、いずれのコマンドでも `--errors-dir path/to/errors` を指定できます。

## Markdownフォーマット

エラー事例は、YAML frontmatter と Markdown のセクションで構成します。`## Error` と `## Solution` は必須で、`## Context` と `## Notes` は任意です。

````markdown
---
id: err_20260526_001
title: Pythonでdotenvが読み込めない
status: resolved
tags:
  - python
  - dotenv
language: Python
frameworks:
  - FastAPI
created_at: 2026-05-26
updated_at: 2026-05-26
---

## Error

```text
ModuleNotFoundError: No module named 'dotenv'
```

## Context

FastAPI 起動時に import で失敗した。

## Solution

```bash
pip install python-dotenv
```

## Notes

使用中の仮想環境も確認する。
````

frontmatter のフィールド:

- `id` (必須): 事例を一意に識別する ID
- `title` (必須): 検索結果に表示する短いタイトル
- `status` (必須): `resolved` など、事例の解決状態
- `tags` (任意): 検索の照合に使用できるタグのリスト
- `language` (任意): 関連するプログラミング言語
- `frameworks` (任意): 関連するフレームワークのリスト
- `created_at` (任意): 事例の作成日
- `updated_at` (任意): 事例の更新日

## なぜLLMを使わないのか

Vol.1 は、同じ入力に対して追跡しやすい結果を返す決定的な仕組みを優先します。完全にオフラインで動作するため API コストや通信要件がなく、どの Markdown 事例と一致理由が解決候補の根拠になったかを確認できます。

## テスト

```bash
pytest tests/ -v
```

## 今後の拡張予定

- LLM を利用した解決候補の整理や説明の補助
- Web UI による検索、閲覧、事例登録
- ベクトルデータベースを用いた意味的な類似検索
- Claude Skill との連携
- Codex による auto-fix ワークフローとの連携
- GitHub Issue や開発記録との連携
