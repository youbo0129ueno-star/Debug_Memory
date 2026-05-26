# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Implement `debug_memory/parser.py` and `tests/test_parser.py`.

The parser reads Markdown files from `memory/errors/*.md`, parses YAML frontmatter, extracts the named sections (`## Error`, `## Context`, `## Solution`, `## Notes`), and returns an `ErrorCase` dataclass.

# Acceptance Criteria

- [ ] `parse_error_case(path: Path) -> ErrorCase` function exists in `debug_memory/parser.py`
- [ ] `load_error_cases(errors_dir: Path) -> list[ErrorCase]` function exists in `debug_memory/parser.py`
- [ ] YAML frontmatter parsing uses `yaml.safe_load` (PyYAML)
- [ ] Extracts `## Error`, `## Context`, `## Solution`, `## Notes` sections from Markdown body
- [ ] Optional sections (Context, Notes) become empty string `""` when absent
- [ ] Required sections (Error, Solution) raise `ValueError` with a clear message when absent
- [ ] Required frontmatter fields (`id`, `title`, `status`) raise `ValueError` when absent
- [ ] Optional frontmatter fields default sanely:
  - `tags: []`
  - `language: None`
  - `frameworks: []`
- [ ] `tests/test_parser.py` has at least these tests (all passing):
  - test that frontmatter is correctly parsed (id, title, status, tags)
  - test that `## Error` content is extracted
  - test that `## Solution` content is extracted
  - test that missing optional sections (Context, Notes) result in empty string
  - test that the 3 sample files in `memory/errors/` all parse without error
- [ ] `pytest tests/test_parser.py -v` exits 0

# Implementation hints

- Frontmatter is delimited by `---` at lines 1 and N (e.g., first 2 occurrences of `---` on their own line)
- Section extraction: split body on `\n## ` (with leading newline) and dispatch by heading name
- Strip section bodies of leading/trailing whitespace
- Code fences inside sections must be preserved
- Use `Path.read_text(encoding="utf-8")`

# Test data location

The 3 sample Markdown files are at:
- `memory/errors/2026-05-26_python-dotenv.md`
- `memory/errors/2026-05-26_fastapi-cors.md`
- `memory/errors/2026-05-26_react-undefined-map.md`

You may create additional fixture files under `tests/fixtures/` if needed for edge cases, but the real sample files should be exercised directly too.

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/debug_memory/parser.py
- /Users/uenoyuuta/Debug_Memory/tests/test_parser.py
- /Users/uenoyuuta/Debug_Memory/tests/fixtures/** (optional)
- /Users/uenoyuuta/Debug_Memory/tests/conftest.py (optional)

# Forbidden Edit Scope

- debug_memory/models.py (already done)
- memory/errors/*.md (do not modify sample data)
- Everything else.

# Verification

```
cd /Users/uenoyuuta/Debug_Memory
source .venv/bin/activate
pip install pytest -q
pytest tests/test_parser.py -v
deactivate
```

Expected: all tests pass, exit 0.

# Final Report Format

```json
{
  "status": "completed | partial | failed",
  "changed_files": [...],
  "summary": "...",
  "tests_run": ["pytest tests/test_parser.py: <N passed>"]
}
```
