# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Implement `debug_memory/signature.py` and `tests/test_signature.py`.

This module extracts searchable features from error log text. It's used both at search time (for the query) and at parse time (against the `## Error` body of stored cases).

# Acceptance Criteria

- [ ] `extract_signature(text: str) -> ErrorSignature` function exists in `debug_memory/signature.py`
- [ ] Extracts:
  - `exception_names`: things matching `\b[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Warning)\b` (e.g., `ModuleNotFoundError`, `TypeError`)
  - `quoted_terms`: contents inside `'...'` and `"..."` (e.g., from `No module named 'dotenv'` → `dotenv`)
  - `package_names`: lowercase-ish identifiers that look like package names — tokens like `python-dotenv`, `fastapi`, `react`, `dotenv`, etc. Heuristic: ASCII-lowercase words possibly with `-` or `_`, length >= 3, that appear in quoted_terms OR appear after `install`/`from`/`import` keywords
  - `commands`: full lines matching `(?:npm|pnpm|yarn|pip|poetry|python|node|docker|git|uv|pytest)\s+[^\n]+` (preserve the command + args)
  - `keywords`: general informative tokens, length >= 4, lowercase, excluding very common English stop words and the items already in other lists
- [ ] Duplicates in any list are removed (preserve insertion order)
- [ ] Case folding: matching is case-insensitive where it makes sense, but `exception_names` preserves original casing
- [ ] Stop-word filter for keywords: at least exclude `the`, `and`, `with`, `from`, `this`, `that`, `have`, `cannot`, `please`, `could`, `would`, `error`, `failed` (extend as needed)
- [ ] `tests/test_signature.py` includes:
  - `ModuleNotFoundError` is extracted as an exception_name
  - `'dotenv'` is extracted as a quoted_term
  - `TypeError` is extracted (from React error message)
  - `npm install foo` is extracted as a command
  - `pip install python-dotenv` is extracted as a command
  - duplicates are deduplicated
- [ ] `pytest tests/test_signature.py -v` exits 0

# Implementation hints

```python
import re

EXCEPTION_PATTERN = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Warning)\b")
QUOTED_PATTERN = re.compile(r"['\"]([^'\"\n]+)['\"]")
COMMAND_PATTERN = re.compile(r"(?:^|\s)((?:npm|pnpm|yarn|pip|poetry|python|node|docker|git|uv|pytest)\s+[^\n]+)", re.MULTILINE)
```

Use a small helper to dedupe while preserving order:
```python
def _dedup(items):
    seen = set()
    out = []
    for x in items:
        key = x.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(x)
    return out
```

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/debug_memory/signature.py
- /Users/uenoyuuta/Debug_Memory/tests/test_signature.py

# Forbidden Edit Scope

- Everything else.

# Verification

```
cd /Users/uenoyuuta/Debug_Memory
source .venv/bin/activate
pytest tests/test_signature.py -v
deactivate
```

Expected: all tests pass.

# Final Report Format

```json
{"status": "completed", "changed_files": [...], "summary": "...", "tests_run": ["pytest tests/test_signature.py: <N passed>"]}
```
