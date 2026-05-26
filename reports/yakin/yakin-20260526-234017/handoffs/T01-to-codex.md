# Role

You are a fresh Codex implementation worker.

You are working under Claude Yakin Agent.
Implement only the scoped task below.
Do not expand scope. Do not refactor unrelated code. Do not switch branches.

# Task

Create the initial project scaffold for Debug Memory Vol.1. This is a Python CLI tool that searches Markdown-based troubleshooting notes (no LLM, no external APIs, no Web UI, no vector DB).

You need to create:
1. `pyproject.toml` for the `debug-memory` package
2. Directory skeleton with `__init__.py` files (no implementation logic yet)
3. `AGENTS.md` for future Codex sessions

# Acceptance Criteria

- [ ] `pyproject.toml` exists at repo root with name = `debug-memory`, Python >= 3.10, deps = `PyYAML`
- [ ] `pyproject.toml` declares `[project.scripts]` entry: `debug-memory = "debug_memory.cli:main"`
- [ ] `debug_memory/` directory created with these empty-but-importable files:
  - `__init__.py` (with `__version__ = "0.1.0"`)
  - `cli.py` (empty stub: `def main(): pass`)
  - `models.py` (empty)
  - `parser.py` (empty)
  - `signature.py` (empty)
  - `search.py` (empty)
  - `rag.py` (empty)
  - `render.py` (empty)
- [ ] `memory/errors/` directory exists (can have a `.gitkeep`)
- [ ] `templates/` directory exists (can have a `.gitkeep`)
- [ ] `tests/` directory exists with `__init__.py`
- [ ] `AGENTS.md` exists at repo root (use the content described in "AGENTS.md content" below)
- [ ] `python -c "import debug_memory; print(debug_memory.__version__)"` prints `0.1.0` after `pip install -e .`

# AGENTS.md content

Write exactly this content to `AGENTS.md`:

```
# AGENTS.md

## Project Overview

This project implements Debug Memory Vol.1: a local CLI tool that searches Markdown-based troubleshooting notes and returns solution candidates for similar software development errors.

## Scope

Implement only the Vol.1 internal system:
- Markdown error case parsing
- Error signature extraction
- Rule-based similar error search
- Solution candidate rendering
- CLI commands: search and ask
- Unit tests

Do not implement:
- Web UI
- LLM API integration
- Vector database
- Claude Skill integration
- Codex auto-fix workflow
- GitHub Issue integration

## Development Guidelines

- Keep the implementation simple and dependency-light.
- Prefer standard library modules where practical.
- Use PyYAML only if needed for frontmatter parsing.
- Use argparse for CLI unless there is a strong reason not to.
- Add tests for parser, signature extraction, search ranking, and answer rendering.
- The tool must work locally without external API calls.
- Search results must include evidence and reasons.
- Do not make the answer sound certain when it is based only on previous similar cases.
```

# Current Repository State

- Branch: ai/yakin-20260526-234017
- Base Branch: main
- Previous status: main initialized with README.md + .gitignore. AI branch created. No source code yet.
- Changed files so far: README.md, .gitignore, reports/yakin/yakin-20260526-234017/state.md (committed on main)

# Completed Work

- None

# Remaining Work

- Create directory structure
- Create pyproject.toml
- Create AGENTS.md
- Create empty Python module files
- Verify package is importable with `pip install -e .`

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/pyproject.toml
- /Users/uenoyuuta/Debug_Memory/AGENTS.md
- /Users/uenoyuuta/Debug_Memory/debug_memory/**
- /Users/uenoyuuta/Debug_Memory/memory/**
- /Users/uenoyuuta/Debug_Memory/templates/**
- /Users/uenoyuuta/Debug_Memory/tests/**

# Forbidden Edit Scope

- README.md (will be done in a later task)
- .gitignore (already done)
- reports/** (managed by Claude PM)
- .env*
- secrets
- credentials
- any other unrelated files

# Constraints

- Keep changes minimal.
- Do NOT write implementation code for parser/signature/search/rag — only empty stubs.
- Do NOT create sample Markdown error cases yet (next task).
- Do not switch branches.
- Do not merge.
- Do not deploy.
- Do not run destructive commands.
- Do not read or write .env files or secrets.
- Do not commit. Claude PM will commit after verification.

# Verification

Run after implementation:

```
cd /Users/uenoyuuta/Debug_Memory
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -c "import debug_memory; print(debug_memory.__version__)"
deactivate
```

Expected result: prints `0.1.0` with no errors.

# Final Report Format

When done, return a JSON block:

```json
{
  "status": "completed | partial | failed",
  "changed_files": ["path/to/file", "..."],
  "summary": "1-3 lines about what was done",
  "tests_run": ["command: result", "..."],
  "unresolved_issues": ["..."],
  "recommended_next_step": "next session should..."
}
```
