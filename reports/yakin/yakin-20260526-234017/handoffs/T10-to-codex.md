# Role

Fresh Codex implementation worker under Claude Yakin Agent.

# Task

Overwrite `/Users/uenoyuuta/Debug_Memory/README.md` with the comprehensive Vol.1 documentation described below.

# Acceptance Criteria

- [ ] README.md exists with the following sections (in this order):
  1. Title `# Debug Memory`
  2. One-paragraph overview (purpose: Markdown-based local CLI for similar-error search)
  3. `## Vol.1 でできること` — bulleted list of features
  4. `## Vol.1 でやらないこと` — bulleted list of explicit non-scope (no LLM, no Web UI, no vector DB, no external API)
  5. `## セットアップ` — venv + `pip install -e .` instructions
  6. `## 使い方` — sample `python -m debug_memory search` and `ask` commands with expected output snippets
  7. `## Markdownフォーマット` — frontmatter + required sections (Error/Solution) + optional (Context/Notes) + frontmatter field list
  8. `## なぜLLMを使わないのか` — short rationale (deterministic, offline, no API cost, traceable)
  9. `## テスト` — `pytest tests/ -v`
  10. `## 今後の拡張予定` — future Vol.2+ ideas (LLM integration, Web UI, vector DB, Claude Skill, Codex auto-fix, etc.)
- [ ] Code samples use proper markdown fenced code blocks
- [ ] No mojibake; use Japanese where natural

# Allowed Edit Scope

- /Users/uenoyuuta/Debug_Memory/README.md

# Forbidden Edit Scope

- Everything else.

# Verification

```
wc -l README.md
head -20 README.md
```

Expected: README.md is at least 50 lines.

# Final Report Format

```json
{"status": "completed", "changed_files": ["README.md"], "summary": "...", "tests_run": []}
```
