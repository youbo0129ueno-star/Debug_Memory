from __future__ import annotations

import re
from collections.abc import Iterable

from .models import ErrorSignature


EXCEPTION_PATTERN = re.compile(
    r"\b[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Warning)\b"
)
QUOTED_PATTERN = re.compile(r"""['"]([^'"\n]+)['"]""")
COMMAND_PATTERN = re.compile(
    r"(?:^|\s)((?:npm|pnpm|yarn|pip|poetry|python|node|docker|git|uv|pytest)"
    r"\s+[^\n]+)",
    re.IGNORECASE | re.MULTILINE,
)
PACKAGE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")
PACKAGE_CONTEXT_PATTERN = re.compile(
    r"\b(?:install|from|import)\s+([a-z][a-z0-9]*(?:[-_][a-z0-9]+)*)\b",
    re.IGNORECASE,
)
TOKEN_PATTERN = re.compile(r"\b[A-Za-z][A-Za-z0-9_-]*\b")

STOP_WORDS = {
    "and",
    "cannot",
    "could",
    "error",
    "failed",
    "from",
    "have",
    "please",
    "that",
    "the",
    "this",
    "with",
    "would",
    "after",
    "before",
    "into",
    "module",
    "named",
}


def _dedup(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def extract_signature(text: str) -> ErrorSignature:
    """Extract ordered, searchable terms from error or query text."""
    exception_names = _dedup(EXCEPTION_PATTERN.findall(text))
    quoted_terms = _dedup(QUOTED_PATTERN.findall(text))
    commands = _dedup(match.group(1).strip() for match in COMMAND_PATTERN.finditer(text))

    package_candidates = [
        term.casefold()
        for term in quoted_terms
        if PACKAGE_PATTERN.fullmatch(term.casefold())
    ]
    package_candidates.extend(
        match.group(1).casefold() for match in PACKAGE_CONTEXT_PATTERN.finditer(text)
    )
    package_names = _dedup(package_candidates)

    represented_tokens: set[str] = set()
    for item in [*exception_names, *quoted_terms, *package_names, *commands]:
        represented_tokens.update(token.casefold() for token in TOKEN_PATTERN.findall(item))

    keywords = _dedup(
        token.casefold()
        for token in TOKEN_PATTERN.findall(text)
        if len(token) >= 4
        and token.casefold() not in STOP_WORDS
        and token.casefold() not in represented_tokens
    )

    return ErrorSignature(
        raw_text=text,
        exception_names=exception_names,
        quoted_terms=quoted_terms,
        package_names=package_names,
        commands=commands,
        keywords=keywords,
    )
