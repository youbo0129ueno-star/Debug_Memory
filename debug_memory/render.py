from __future__ import annotations

from .models import SearchResult


def render_search_results(results: list[SearchResult]) -> str:
    """Render ranked matches and the evidence supporting each result."""
    lines = ["Search Results", "==============", ""]
    if not results:
        lines.append("(no matches)")
        return "\n".join(lines)

    for index, result in enumerate(results, start=1):
        lines.extend(
            [
                f"[{index}] {result.case.title}",
                f"    score: {result.score:.3f}",
                f"    status: {result.case.status}",
                f"    tags: {', '.join(result.case.tags)}",
                f"    file: {result.case.path}",
                "    reasons:",
            ]
        )
        if result.reasons:
            lines.extend(f"    - {reason}" for reason in result.reasons)
        else:
            lines.append("    - (none)")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_answer(answer: str) -> str:
    """Return an already-built answer for callers needing a render hook."""
    return answer
