## Status

- Status: running
- Run ID: yakin-20260526-234017
- Started At: 2026-05-26T23:40:17+09:00
- Target Repository: youbo0129ueno-star/Debug_Memory
- Base Branch: main
- AI Work Branch: ai/yakin-20260526-234017
- Notion Report Page: (pending)

## Goal

Debug Memory Vol.1 を実装する: Markdownベースのローカルエラー検索CLIツール (Python製，LLM/外部API不使用)．`python -m debug_memory search` と `ask` の2コマンド + pytest を完成させる．

## Task Queue

| Task ID | Title | Status | Notes |
|---------|-------|--------|-------|
| T01 | プロジェクト雛形 (pyproject.toml, dirs, AGENTS.md) | planned | |
| T02 | サンプルMarkdown 3件 + templates/error_case.md | planned | |
| T03 | models.py (dataclass定義) | planned | |
| T04 | parser.py + test_parser.py | planned | |
| T05 | signature.py + test_signature.py | planned | |
| T06 | search.py + test_search.py | planned | |
| T07 | rag.py + test_rag.py | planned | |
| T08 | render.py + cli.py | planned | |
| T09 | 完成条件動作確認 (ask実走 + pytest全通過) | planned | |
| T10 | README.md 整備 | planned | |

## Safety Rules

- Work only on the AI branch `ai/yakin-20260526-234017`.
- Never merge into main.
- Never push to main (after initial bootstrap).
- Never deploy.
- Never read secrets or `.env`.
- Stop on auth/billing/permissions/migrations/infra ambiguity.
- Stop on broad test failures or conflicts.

## Progress

| Time | Event | Details |
|------|-------|---------|
| 2026-05-26T23:40:17+09:00 | Run started | Run ID: yakin-20260526-234017 |
| 2026-05-26T23:42:00+09:00 | main initialized | README + .gitignore committed and pushed |
| 2026-05-26T23:42:30+09:00 | AI branch created | ai/yakin-20260526-234017 pushed |

## Codex Sessions

| Session | Task | Status | Notes |
|---------|------|--------|-------|

## Capacity Notes

- Claude: 観測中
- Codex: 観測中 (v0.133.0)
- Warnings: なし

## Reports

- Notion Report: (pending)
- Summary: reports/yakin/yakin-20260526-234017/summary.md
- Metrics: reports/yakin/yakin-20260526-234017/metrics.md
- State: reports/yakin/yakin-20260526-234017/state.md
- Handoffs: reports/yakin/yakin-20260526-234017/handoffs/
- Codex Reports: reports/yakin/yakin-20260526-234017/codex-reports/
- Diffs: reports/yakin/yakin-20260526-234017/diffs/
- Logs: reports/yakin/yakin-20260526-234017/logs/

## Human Review Needed

(in progress)

## Latest Recommended Action

(in progress)
