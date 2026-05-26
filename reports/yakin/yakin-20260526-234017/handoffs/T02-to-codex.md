# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Create 3 sample Markdown error case files and 1 template file for Debug Memory Vol.1.

These files will be the seed data for the search engine. They follow a strict frontmatter + Markdown format described below.

# Acceptance Criteria

- [ ] `memory/errors/2026-05-26_python-dotenv.md` exists with the content below
- [ ] `memory/errors/2026-05-26_fastapi-cors.md` exists with the content below
- [ ] `memory/errors/2026-05-26_react-undefined-map.md` exists with the content below
- [ ] `templates/error_case.md` exists with the template content below
- [ ] `memory/errors/.gitkeep` is removed (since we now have real files)
- [ ] All files start with `---` YAML frontmatter and contain `## Error` and `## Solution` sections

# File contents

### memory/errors/2026-05-26_python-dotenv.md

```markdown
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
```

### memory/errors/2026-05-26_fastapi-cors.md

```markdown
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
```

### memory/errors/2026-05-26_react-undefined-map.md

```markdown
---
id: err_20260526_003
title: ReactでCannot read properties of undefined (reading 'map')
status: resolved
tags:
  - react
  - javascript
  - typescript
language: JavaScript
frameworks:
  - React
created_at: 2026-05-26
updated_at: 2026-05-26
---

## Error

```text
TypeError: Cannot read properties of undefined (reading 'map')
```

## Context

API から取得したデータを `data.map(...)` でレンダリングしたときに発生。初回レンダリング時はまだ fetch が完了しておらず、`data` が `undefined` のため map が呼べない。

## Solution

3つのアプローチがある:

1. **初期値を空配列にする**
   ```javascript
   const [data, setData] = useState([])
   ```

2. **Optional chaining を使う**
   ```javascript
   {data?.map((item) => <Item key={item.id} {...item} />)}
   ```

3. **Loading状態を確認する**
   ```javascript
   if (loading) return <Spinner />
   if (!data) return null
   return data.map(...)
   ```

## Notes

TypeScript を使っているなら `data: Item[] | undefined` のように型を明示すると、コンパイラがガード忘れを検出してくれる。
```

### templates/error_case.md

```markdown
---
id: err_YYYYMMDD_NNN
title: <短い1行タイトル>
status: resolved
tags:
  - <tag1>
  - <tag2>
language: <Python | JavaScript | TypeScript | Go | ...>
frameworks:
  - <Framework名>
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

## Error

```text
<エラーメッセージそのまま>
```

## Context

<どういう状況で発生したか>

## Solution

<解決手順>

## Notes

<補足，仮想環境の確認方法，関連リンク等>
```

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/memory/errors/*.md
- /Users/uenoyuuta/Debug_Memory/templates/error_case.md
- /Users/uenoyuuta/Debug_Memory/memory/errors/.gitkeep (delete)

# Forbidden Edit Scope

- Everything else.

# Constraints

- Write file contents EXACTLY as specified. Do not paraphrase or "improve" the markdown.
- Do not commit. Claude PM will commit.

# Verification

```
ls -la memory/errors/ templates/
head -15 memory/errors/2026-05-26_python-dotenv.md
```

Expected: 3 .md files in memory/errors/ (no .gitkeep), 1 error_case.md in templates/.

# Final Report Format

```json
{
  "status": "completed | partial | failed",
  "changed_files": [...],
  "summary": "...",
  "tests_run": ["...: result"]
}
```
