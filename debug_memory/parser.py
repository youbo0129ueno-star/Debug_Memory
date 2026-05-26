from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .models import ErrorCase


_FRONTMATTER_DELIMITER = "---"
_SECTION_PATTERN = re.compile(
    r"^##[ \t]+(Error|Context|Solution|Notes)[ \t]*\n(.*?)(?=^##[ \t]+|\Z)",
    re.MULTILINE | re.DOTALL,
)
_REQUIRED_FIELDS = ("id", "title", "status")
_REQUIRED_SECTIONS = ("Error", "Solution")


def _split_frontmatter(text: str, path: Path) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FRONTMATTER_DELIMITER:
        raise ValueError(f"{path}: YAML frontmatter must start with '---'")

    try:
        closing_delimiter = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == _FRONTMATTER_DELIMITER
        )
    except StopIteration as exc:
        raise ValueError(f"{path}: YAML frontmatter is missing closing '---'") from exc

    frontmatter_text = "\n".join(lines[1:closing_delimiter])
    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML frontmatter: {exc}") from exc

    if not isinstance(metadata, dict):
        raise ValueError(f"{path}: YAML frontmatter must be a mapping")

    body = "\n".join(lines[closing_delimiter + 1 :])
    return metadata, body


def _extract_sections(body: str, path: Path) -> dict[str, str]:
    sections = {
        heading: content.strip()
        for heading, content in _SECTION_PATTERN.findall(body)
    }
    for heading in _REQUIRED_SECTIONS:
        if heading not in sections:
            raise ValueError(f"{path}: required Markdown section '## {heading}' is missing")
    return sections


def parse_error_case(path: Path) -> ErrorCase:
    """Parse one Markdown troubleshooting note into an ErrorCase."""
    metadata, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)

    for field in _REQUIRED_FIELDS:
        if field not in metadata or metadata[field] is None:
            raise ValueError(f"{path}: required frontmatter field '{field}' is missing")

    sections = _extract_sections(body, path)
    return ErrorCase(
        id=str(metadata["id"]),
        title=str(metadata["title"]),
        status=str(metadata["status"]),
        tags=list(metadata.get("tags") or []),
        language=metadata.get("language"),
        frameworks=list(metadata.get("frameworks") or []),
        error=sections["Error"],
        context=sections.get("Context", ""),
        solution=sections["Solution"],
        notes=sections.get("Notes", ""),
        path=path,
    )


def load_error_cases(errors_dir: Path) -> list[ErrorCase]:
    """Parse all Markdown troubleshooting notes in an error memory directory."""
    return [parse_error_case(path) for path in sorted(errors_dir.glob("*.md"))]
