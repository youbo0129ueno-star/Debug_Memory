# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Implement `debug_memory/rag.py` and `tests/test_rag.py`.

This module assembles the textual "answer" from search results. **No LLM, no external API.** It takes the top-K search results, prefers the highest-scored `resolved` case with a non-empty solution, and formats the output exactly as specified in the spec.

# Acceptance Criteria

- [ ] `build_answer(query: str, results: list[SearchResult]) -> str` exists in `debug_memory/rag.py`
- [ ] Output starts with the header `Debug Memory Answer` followed by `===================`
- [ ] Includes the `Input:` line with the query
- [ ] If at least one resolved result with non-empty `case.solution` exists:
  - Picks the highest-scored such result as the "Top solution candidate"
  - Outputs `Top solution candidate: <title>`
  - Outputs `Solution:` followed by the case's `solution` field
  - Outputs `Notes:` followed by the case's `notes` field (if non-empty)
  - Outputs `Evidence:` section listing top results (up to all in `results`), each entry showing:
    - index, title
    - file: relative path or path basename
    - status, score
    - reasons (bulleted, indented)
- [ ] If no resolved-with-solution result exists:
  - Outputs `No resolved solution candidate found.`
  - Outputs `Similar unresolved cases:` list (or `(none)` if results empty)
  - Outputs `Suggestion: 過去の解決済み事例は見つかりませんでした。新しいエラー事例としてMarkdownに記録してください。`
- [ ] Uses cautious language — does NOT say "これが原因です" or similar — phrasing like "過去の類似事例では、以下の解決策で解決しています" is OK
- [ ] `tests/test_rag.py` includes (using sample data loaded via `load_error_cases` + `search_similar_cases`):
  - For a dotenv query, the output contains "pip install python-dotenv"
  - For a dotenv query, the output contains an Evidence section
  - For a query that matches nothing, the output contains "No resolved solution candidate found"
- [ ] `pytest tests/test_rag.py -v` exits 0

# Output shape example

```
Debug Memory Answer
===================

Input:
ModuleNotFoundError: No module named 'dotenv'

Found 1 similar case.

Top solution candidate:
Pythonでdotenvが読み込めない

Solution:
pip install python-dotenv

Notes:
仮想環境が違う場合もあるので、which python と pip list を確認する。

Evidence:
[1] Pythonでdotenvが読み込めない
    file: 2026-05-26_python-dotenv.md
    status: resolved
    score: 0.92
    reasons:
    - exception matched: ModuleNotFoundError
    - quoted term matched: dotenv
    - status bonus: resolved
```

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/debug_memory/rag.py
- /Users/uenoyuuta/Debug_Memory/tests/test_rag.py

# Forbidden Edit Scope

- Everything else.

# Verification

```
cd /Users/uenoyuuta/Debug_Memory
source .venv/bin/activate
pytest tests/test_rag.py -v
deactivate
```

# Final Report Format

```json
{"status": "completed", "changed_files": [...], "summary": "...", "tests_run": [...]}
```
