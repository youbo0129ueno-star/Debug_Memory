# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Implement `debug_memory/render.py` and `debug_memory/cli.py`.

These wire everything together into a usable CLI: `python -m debug_memory search --text "..."` and `python -m debug_memory ask --text "..."`.

# Acceptance Criteria

- [ ] `debug_memory/cli.py` exposes `main()` and the file is invokable as `python -m debug_memory ...`
- [ ] To make `python -m debug_memory` work, create or edit `debug_memory/__main__.py` to call `main()` from `cli.py`
- [ ] `argparse`-based CLI with two subcommands:
  - `search --text "<error log>" [--top-k N] [--errors-dir PATH]`
  - `ask    --text "<error log>" [--top-k N] [--errors-dir PATH]`
- [ ] Defaults: `--top-k = 3`, `--errors-dir = memory/errors`
- [ ] `--errors-dir` resolves relative to current working directory (Path.cwd())
- [ ] `search` prints output starting with `Search Results` header and `==============`, then a numbered list of results showing title, score, status, tags, file path, and reasons (indented)
- [ ] `ask` prints the output from `build_answer(...)`
- [ ] If no cases are found in `--errors-dir`, both commands print a clear "no cases found at <dir>" message and exit non-zero
- [ ] `debug_memory/render.py` contains:
  - `render_search_results(results: list[SearchResult]) -> str` — the search subcommand uses this
  - (Optional) `render_answer(answer: str) -> str` — passthrough or formatting helper
- [ ] Both subcommands work end-to-end with the sample data:
  - `python -m debug_memory search --text "ModuleNotFoundError: No module named 'dotenv'"` shows the python-dotenv case as #1
  - `python -m debug_memory ask --text "ModuleNotFoundError: No module named 'dotenv'"` shows "pip install python-dotenv" in the Solution block

# Implementation hints

`debug_memory/__main__.py`:
```python
from debug_memory.cli import main

if __name__ == "__main__":
    main()
```

`debug_memory/cli.py`:
```python
import argparse
import sys
from pathlib import Path

from debug_memory.parser import load_error_cases
from debug_memory.search import search_similar_cases
from debug_memory.rag import build_answer
from debug_memory.render import render_search_results


def _common_args(p):
    p.add_argument("--text", required=True)
    p.add_argument("--top-k", type=int, default=3)
    p.add_argument("--errors-dir", default="memory/errors")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="debug-memory")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s_search = sub.add_parser("search")
    _common_args(s_search)
    s_ask = sub.add_parser("ask")
    _common_args(s_ask)

    args = parser.parse_args(argv)
    errors_dir = Path(args.errors_dir)
    cases = load_error_cases(errors_dir)
    if not cases:
        print(f"no cases found at {errors_dir}", file=sys.stderr)
        return 2
    results = search_similar_cases(args.text, cases, top_k=args.top_k)
    if args.cmd == "search":
        print(render_search_results(results))
    else:
        print(build_answer(args.text, results))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
```

`debug_memory/render.py`:
```python
def render_search_results(results):
    lines = ["Search Results", "==============", ""]
    if not results:
        lines.append("(no matches)")
        return "\n".join(lines)
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r.case.title}")
        lines.append(f"    score: {r.score}")
        lines.append(f"    status: {r.case.status}")
        lines.append(f"    tags: {', '.join(r.case.tags)}")
        lines.append(f"    file: {r.case.path}")
        lines.append(f"    reasons:")
        for reason in r.reasons:
            lines.append(f"    - {reason}")
        lines.append("")
    return "\n".join(lines).rstrip()
```

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/debug_memory/cli.py
- /Users/uenoyuuta/Debug_Memory/debug_memory/__main__.py
- /Users/uenoyuuta/Debug_Memory/debug_memory/render.py

# Forbidden Edit Scope

- Everything else, especially debug_memory/parser.py, search.py, rag.py, signature.py, models.py.

# Verification

```
cd /Users/uenoyuuta/Debug_Memory
source .venv/bin/activate
python -m debug_memory search --text "ModuleNotFoundError: No module named 'dotenv'" | head -20
python -m debug_memory ask --text "ModuleNotFoundError: No module named 'dotenv'" | head -30
deactivate
```

Expected:
- `search` output includes the python-dotenv case as #1 with reasons
- `ask` output includes `pip install python-dotenv`

# Final Report Format

```json
{"status": "completed", "changed_files": [...], "summary": "...", "tests_run": [...]}
```
