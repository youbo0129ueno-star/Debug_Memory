# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Fix a small pyproject.toml issue blocking `pip install -e .`.

The current pyproject.toml uses setuptools flat-layout auto-discovery, which picks up `memory/`, `reports/`, `templates/` as top-level packages and refuses to build.

Fix: explicitly declare only `debug_memory` as the package via `[tool.setuptools.packages.find]` with `include = ["debug_memory*"]`, OR via explicit `packages = ["debug_memory"]`.

# Acceptance Criteria

- [ ] `pip install -e .` succeeds inside the existing `.venv/`
- [ ] `python -c "import debug_memory; print(debug_memory.__version__)"` still prints `0.1.0`
- [ ] Only pyproject.toml is modified

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/pyproject.toml

# Forbidden Edit Scope

- Everything else.

# Verification

```
cd /Users/uenoyuuta/Debug_Memory
source .venv/bin/activate
pip install -e . 2>&1 | tail -5
python -c "import debug_memory; print(debug_memory.__version__)"
deactivate
```

Expected: install succeeds, prints `0.1.0`.

# Final Report Format

```json
{
  "status": "completed | partial | failed",
  "changed_files": ["pyproject.toml"],
  "summary": "...",
  "tests_run": ["...: result"]
}
```
