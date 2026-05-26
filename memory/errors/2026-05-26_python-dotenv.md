---
id: err_20260526_001
title: Pythonでdotenvが読み込めない
status: resolved
tags:
  - python
  - dotenv
  - venv
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

venvを作り直したあと、FastAPI起動時に発生。`from dotenv import load_dotenv` の行で落ちる。

## Solution

```bash
pip install python-dotenv
```

パッケージ名は `dotenv` ではなく `python-dotenv`。インポート名と pip パッケージ名が違うので注意。

## Notes

仮想環境が違う場合もあるので、`which python` と `pip list` を確認する。VSCode などのIDEで別の venv を指している場合も多い。
