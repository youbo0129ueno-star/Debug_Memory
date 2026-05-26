# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Implement `debug_memory/search.py` and `tests/test_search.py`.

This is the rule-based similarity search engine. It scores each stored `ErrorCase` against a query string using its `ErrorSignature` and metadata, then returns the top-K results with reasons.

# Acceptance Criteria

- [ ] `search_similar_cases(query: str, cases: list[ErrorCase], top_k: int = 3) -> list[SearchResult]` exists in `debug_memory/search.py`
- [ ] Uses `extract_signature` from `debug_memory.signature` on both the query and each case's `error` field
- [ ] Scoring rules (weights as listed, may microtune by ±20%):
  - exception_name match: +0.35 per match (cap at 1 match counted)
  - quoted_term match: +0.25
  - package_name match: +0.20
  - tag match (between query keywords and case.tags): +0.12
  - language match (query mentions language string and case.language matches): +0.08
  - framework match: +0.08
  - keyword match: +0.02 per match (cap at 5 matches counted = +0.10)
  - status=='resolved' bonus: +0.10
- [ ] Each `SearchResult.reasons` is a non-empty list of human-readable strings like:
  - `"exception matched: ModuleNotFoundError"`
  - `"quoted term matched: dotenv"`
  - `"tag matched: python"`
  - `"status bonus: resolved"`
- [ ] Cases with score == 0 are excluded from results
- [ ] Results are sorted by score descending, then by id ascending (stable tie-break)
- [ ] Returns at most `top_k` results (default 3)
- [ ] `tests/test_search.py` includes (using the 3 sample files loaded via `load_error_cases`):
  - dotenv query → python-dotenv case is #1
  - CORS query → fastapi-cors case is #1
  - React undefined map query → react-undefined-map case is #1
  - resolved cases get the resolved bonus (verify reasons contains "status bonus: resolved")
  - reasons list is non-empty for top result
- [ ] `pytest tests/test_search.py -v` exits 0

# Implementation hints

```python
from debug_memory.models import ErrorCase, SearchResult
from debug_memory.signature import extract_signature

def search_similar_cases(query, cases, top_k=3):
    q_sig = extract_signature(query)
    results = []
    for case in cases:
        c_sig = extract_signature(case.error + "\n" + case.title)
        score = 0.0
        reasons = []
        # exception name overlap
        for e in q_sig.exception_names:
            if e in c_sig.exception_names:
                score += 0.35
                reasons.append(f"exception matched: {e}")
                break
        # quoted term overlap
        for t in q_sig.quoted_terms:
            if t.lower() in [x.lower() for x in c_sig.quoted_terms]:
                score += 0.25
                reasons.append(f"quoted term matched: {t}")
                break
        # ... etc
        # status bonus
        if case.status == "resolved":
            score += 0.10
            reasons.append("status bonus: resolved")
        if score > 0:
            results.append(SearchResult(case=case, score=round(score, 3), reasons=reasons))
    results.sort(key=lambda r: (-r.score, r.case.id))
    return results[:top_k]
```

Adapt as needed — this is just a sketch.

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/debug_memory/search.py
- /Users/uenoyuuta/Debug_Memory/tests/test_search.py

# Forbidden Edit Scope

- Everything else.

# Verification

```
cd /Users/uenoyuuta/Debug_Memory
source .venv/bin/activate
pytest tests/test_search.py -v
deactivate
```

# Final Report Format

```json
{"status": "completed", "changed_files": [...], "summary": "...", "tests_run": [...]}
```
