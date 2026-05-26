#!/bin/bash
# run-task.sh — 1タスク完結スクリプト (codex実行 + 検収 + commit + push)
# Usage: bash run-task.sh <TASK_ID> "<commit message>" "<verify_cmd>"
# Example: bash run-task.sh T04 "feat(T04): parser + tests" "pytest tests/test_parser.py -v"

set -uo pipefail

TASK_ID="${1:?task id required}"
COMMIT_MSG="${2:?commit message required}"
VERIFY_CMD="${3:-}"

RUN_ID="yakin-20260526-234017"
REPO="/Users/uenoyuuta/Debug_Memory"
REPORT_DIR="${REPO}/reports/yakin/${RUN_ID}"
HANDOFF="${REPORT_DIR}/handoffs/${TASK_ID}-to-codex.md"
LOG_DIR="${REPORT_DIR}/logs"
DIFF_DIR="${REPORT_DIR}/diffs"
CODEX_DIR="${REPORT_DIR}/codex-reports"

mkdir -p "$LOG_DIR" "$DIFF_DIR" "$CODEX_DIR"
cd "$REPO"

# Branch safety
BRANCH=$(git branch --show-current)
for prot in main master develop production staging; do
  if [ "$BRANCH" = "$prot" ]; then
    echo "ERROR: refused — protected branch: $BRANCH" >&2
    exit 99
  fi
done
echo "=== ${TASK_ID} on ${BRANCH} ===" >&2

# 1. Codex exec
echo "[1/4] codex exec..." >&2
codex exec -C "$REPO" -s workspace-write --skip-git-repo-check \
  < "$HANDOFF" \
  > "${LOG_DIR}/${TASK_ID}.stdout.log" \
  2> "${LOG_DIR}/${TASK_ID}.stderr.log"
CODEX_EXIT=$?
echo "  codex exit=${CODEX_EXIT}" >&2

# Diff snapshot
git diff --stat > "${DIFF_DIR}/${TASK_ID}.diffstat" 2>/dev/null || true
git diff --name-only > "${DIFF_DIR}/${TASK_ID}.changed-files" 2>/dev/null || true

# 2. Verify
VERIFY_RESULT="skipped"
if [ -n "$VERIFY_CMD" ]; then
  echo "[2/4] verify: $VERIFY_CMD" >&2
  if source .venv/bin/activate 2>/dev/null; then :; fi
  if bash -c "$VERIFY_CMD" > "${LOG_DIR}/${TASK_ID}.verify.log" 2>&1; then
    VERIFY_RESULT="passed"
    echo "  verify PASSED" >&2
  else
    VERIFY_RESULT="failed"
    echo "  verify FAILED — tail:" >&2
    tail -30 "${LOG_DIR}/${TASK_ID}.verify.log" >&2
  fi
  deactivate 2>/dev/null || true
fi

# 3. Codex report
{
  echo "# Codex Report: ${TASK_ID}"
  echo
  echo "- Branch: ${BRANCH}"
  echo "- Codex Exit: ${CODEX_EXIT}"
  echo "- Verify: ${VERIFY_RESULT}"
  echo
  echo "## Changed files"
  echo '```'
  cat "${DIFF_DIR}/${TASK_ID}.changed-files" 2>/dev/null || true
  git diff --cached --name-only 2>/dev/null
  echo '```'
  echo
  echo "## Codex stdout (tail 80)"
  echo '```'
  tail -80 "${LOG_DIR}/${TASK_ID}.stdout.log" 2>/dev/null || true
  echo '```'
} > "${CODEX_DIR}/${TASK_ID}-report.md"

# 4. Commit + push (only if verify is passed or skipped)
if [ "$VERIFY_RESULT" = "failed" ]; then
  echo "[3/4] SKIP commit — verify failed" >&2
  echo "[4/4] DONE (no push)" >&2
  exit 2
fi

if [ "$CODEX_EXIT" -ne 0 ]; then
  echo "[3/4] SKIP commit — codex failed (exit ${CODEX_EXIT})" >&2
  exit 3
fi

echo "[3/4] git add + commit + push" >&2
# Stage everything that's modified or new under non-secret dirs
git add -- debug_memory tests memory templates pyproject.toml AGENTS.md README.md 2>/dev/null || true
git add -- "${REPORT_DIR}" 2>/dev/null || true

if git diff --cached --quiet; then
  echo "  no staged changes — skipping commit" >&2
else
  git -c user.email=youbo0129ueno@gmail.com -c user.name=youbo0129ueno-star \
    commit -m "$COMMIT_MSG" > "${LOG_DIR}/${TASK_ID}.commit.log" 2>&1
  git push > "${LOG_DIR}/${TASK_ID}.push.log" 2>&1 || true
  echo "  pushed: $(git log -1 --pretty=oneline)" >&2
fi

echo "[4/4] DONE ${TASK_ID}" >&2
exit 0
