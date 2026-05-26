from __future__ import annotations

import re

from .models import ErrorCase, SearchResult
from .signature import extract_signature


def _overlap(left: list[str], right: list[str]) -> list[str]:
    right_terms = {term.casefold() for term in right}
    return [term for term in left if term.casefold() in right_terms]


def _mentioned(query: str, term: str) -> bool:
    if not term:
        return False
    pattern = rf"(?<![\w-]){re.escape(term)}(?![\w-])"
    return re.search(pattern, query, re.IGNORECASE) is not None


def search_similar_cases(
    query: str, cases: list[ErrorCase], top_k: int = 3
) -> list[SearchResult]:
    """Return the highest-scoring previous cases related to a query."""
    if top_k <= 0:
        return []

    query_signature = extract_signature(query)
    results: list[SearchResult] = []

    for case in cases:
        case_signature = extract_signature(case.error)
        score = 0.0
        reasons: list[str] = []

        exception_matches = _overlap(
            query_signature.exception_names, case_signature.exception_names
        )
        if exception_matches:
            score += 0.35
            reasons.append(f"exception matched: {exception_matches[0]}")

        quoted_matches = _overlap(
            query_signature.quoted_terms, case_signature.quoted_terms
        )
        if quoted_matches:
            score += 0.25
            reasons.append(f"quoted term matched: {quoted_matches[0]}")

        package_matches = _overlap(
            query_signature.package_names, case_signature.package_names
        )
        if package_matches:
            score += 0.20
            reasons.append(f"package matched: {package_matches[0]}")

        tag_matches = _overlap(query_signature.keywords, case.tags)
        if tag_matches:
            score += 0.12
            reasons.append(f"tag matched: {tag_matches[0]}")

        if case.language and _mentioned(query, case.language):
            score += 0.08
            reasons.append(f"language matched: {case.language}")

        framework_match = next(
            (framework for framework in case.frameworks if _mentioned(query, framework)),
            None,
        )
        if framework_match:
            score += 0.08
            reasons.append(f"framework matched: {framework_match}")

        for keyword in _overlap(query_signature.keywords, case_signature.keywords)[:5]:
            score += 0.02
            reasons.append(f"keyword matched: {keyword}")

        if case.status.casefold() == "resolved":
            score += 0.10
            reasons.append("status bonus: resolved")

        if score > 0:
            results.append(
                SearchResult(case=case, score=round(score, 3), reasons=reasons)
            )

    results.sort(key=lambda result: (-result.score, result.case.id))
    return results[:top_k]
