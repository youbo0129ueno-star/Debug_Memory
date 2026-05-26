from __future__ import annotations

from .models import SearchResult


_NO_SOLUTION_SUGGESTION = (
    "Suggestion: 過去の解決済み事例は見つかりませんでした。"
    "新しいエラー事例としてMarkdownに記録してください。"
)


def _format_result(result: SearchResult, index: int) -> list[str]:
    lines = [
        f"[{index}] {result.case.title}",
        f"    file: {result.case.path.name}",
        f"    status: {result.case.status}",
        f"    score: {result.score:.2f}",
        "    reasons:",
    ]
    if result.reasons:
        lines.extend(f"    - {reason}" for reason in result.reasons)
    else:
        lines.append("    - (none)")
    return lines


def build_answer(query: str, results: list[SearchResult]) -> str:
    """Render cautious, evidence-backed guidance from previous error cases."""
    lines = [
        "Debug Memory Answer",
        "===================",
        "",
        "Input:",
        query,
        "",
    ]
    count = len(results)
    suffix = "case" if count == 1 else "cases"
    lines.extend([f"Found {count} similar {suffix}.", ""])

    candidates = [
        result
        for result in results
        if result.case.status.casefold() == "resolved"
        and result.case.solution.strip()
    ]

    if candidates:
        top_candidate = max(candidates, key=lambda result: result.score)
        lines.extend(
            [
                "Top solution candidate:",
                top_candidate.case.title,
                "",
                "Solution:",
                top_candidate.case.solution,
            ]
        )
        if top_candidate.case.notes.strip():
            lines.extend(["", "Notes:", top_candidate.case.notes])
        lines.extend(["", "Evidence:"])
        for index, result in enumerate(results, start=1):
            lines.extend(_format_result(result, index))
        return "\n".join(lines)

    lines.extend(
        [
            "No resolved solution candidate found.",
            "",
            "Similar unresolved cases:",
        ]
    )
    if results:
        for index, result in enumerate(results, start=1):
            lines.extend(_format_result(result, index))
    else:
        lines.append("(none)")
    lines.extend(["", _NO_SOLUTION_SUGGESTION])
    return "\n".join(lines)
