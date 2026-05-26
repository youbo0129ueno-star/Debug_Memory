# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Implement `debug_memory/models.py` with dataclass definitions for the entire Debug Memory Vol.1 internal data model.

# Acceptance Criteria

- [ ] `debug_memory/models.py` contains the following dataclasses:
  - `ErrorCase` (id, title, status, tags, language, frameworks, error, context, solution, notes, path)
  - `ErrorSignature` (raw_text, exception_names, quoted_terms, package_names, commands, keywords)
  - `SearchResult` (case, score, reasons)
- [ ] All dataclasses are decorated with `@dataclass`
- [ ] Use `from __future__ import annotations` at the top
- [ ] Use modern Python 3.10+ syntax: `list[str]`, `str | None`, etc.
- [ ] `language` field of `ErrorCase` is `str | None` (optional)
- [ ] `path` field of `ErrorCase` is `pathlib.Path`
- [ ] `from dataclasses import dataclass` and `from pathlib import Path` imports present
- [ ] No business logic in this file — only dataclass definitions
- [ ] `python -c "from debug_memory.models import ErrorCase, ErrorSignature, SearchResult; print('ok')"` prints `ok`

# Exact dataclass shape

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ErrorCase:
    id: str
    title: str
    status: str
    tags: list[str]
    language: str | None
    frameworks: list[str]
    error: str
    context: str
    solution: str
    notes: str
    path: Path


@dataclass
class ErrorSignature:
    raw_text: str
    exception_names: list[str]
    quoted_terms: list[str]
    package_names: list[str]
    commands: list[str]
    keywords: list[str]


@dataclass
class SearchResult:
    case: ErrorCase
    score: float
    reasons: list[str]
```

You may optionally add a `RagAnswer` dataclass if it would help T07 (`rag.py`), but it is not required for this task.

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/debug_memory/models.py

# Forbidden Edit Scope

- Everything else.

# Verification

```
cd /Users/uenoyuuta/Debug_Memory
source .venv/bin/activate
python -c "from debug_memory.models import ErrorCase, ErrorSignature, SearchResult; print('ok')"
deactivate
```

Expected: prints `ok`.

# Final Report Format

```json
{
  "status": "completed | partial | failed",
  "changed_files": ["debug_memory/models.py"],
  "summary": "...",
  "tests_run": ["...: result"]
}
```
