from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ErrorCase:
    id: str
    title: str
    status: str
    tags: list[str]
    language: str | None
    frameworks: list[str]
    error: str
    context: str
    solution: str
    notes: str
    path: Path


@dataclass
class ErrorSignature:
    raw_text: str
    exception_names: list[str]
    quoted_terms: list[str]
    package_names: list[str]
    commands: list[str]
    keywords: list[str]


@dataclass
class SearchResult:
    case: ErrorCase
    score: float
    reasons: list[str]
