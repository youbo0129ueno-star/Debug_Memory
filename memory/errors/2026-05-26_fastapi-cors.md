---
id: err_20260526_002
title: FastAPIでCORSエラーが出る
status: resolved
tags:
  - fastapi
  - cors
  - python
language: Python
frameworks:
  - FastAPI
created_at: 2026-05-26
updated_at: 2026-05-26
---

## Error

```text
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Context

Next.js (port 3000) フロントエンドから FastAPI (port 8000) バックエンドを fetch したときにブラウザのコンソールで発生。

## Solution

CORSMiddleware を FastAPI アプリに追加する:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Notes

本番では `allow_origins=["*"]` は避け、明示的にドメインを列挙する。`allow_credentials=True` のときは `allow_origins=["*"]` が無効になる仕様にも注意。
