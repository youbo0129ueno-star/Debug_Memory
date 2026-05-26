from pathlib import Path

import pytest

from debug_memory.parser import load_error_cases, parse_error_case


ERRORS_DIR = Path(__file__).parent.parent / "memory" / "errors"


def _write_case(tmp_path: Path, body: str, frontmatter: str | None = None) -> Path:
    metadata = frontmatter or """\
id: err_test
title: Test error
status: resolved
tags:
  - python
  - parsing
"""
    path = tmp_path / "case.md"
    path.write_text(f"---\n{metadata}---\n\n{body}", encoding="utf-8")
    return path


def test_frontmatter_is_parsed(tmp_path: Path) -> None:
    path = _write_case(
        tmp_path,
        "## Error\n\nbroken\n\n## Solution\n\nfixed\n",
    )

    case = parse_error_case(path)

    assert case.id == "err_test"
    assert case.title == "Test error"
    assert case.status == "resolved"
    assert case.tags == ["python", "parsing"]


def test_error_content_is_extracted_and_preserves_code_fences(tmp_path: Path) -> None:
    path = _write_case(
        tmp_path,
        "## Error\n\n```text\nModuleNotFoundError: dotenv\n```\n\n## Solution\n\ninstall it\n",
    )

    assert parse_error_case(path).error == "```text\nModuleNotFoundError: dotenv\n```"


def test_solution_content_is_extracted(tmp_path: Path) -> None:
    path = _write_case(
        tmp_path,
        "## Error\n\nbroken\n\n## Solution\n\n```bash\npip install python-dotenv\n```\n",
    )

    assert parse_error_case(path).solution == "```bash\npip install python-dotenv\n```"


def test_missing_optional_sections_and_metadata_use_defaults(tmp_path: Path) -> None:
    path = _write_case(
        tmp_path,
        "## Error\n\nbroken\n\n## Solution\n\nfixed\n",
        frontmatter="id: err_minimal\ntitle: Minimal\nstatus: open\n",
    )

    case = parse_error_case(path)

    assert case.context == ""
    assert case.notes == ""
    assert case.tags == []
    assert case.language is None
    assert case.frameworks == []


@pytest.mark.parametrize("section", ["Error", "Solution"])
def test_missing_required_section_raises_value_error(tmp_path: Path, section: str) -> None:
    included_section = "Solution" if section == "Error" else "Error"
    path = _write_case(tmp_path, f"## {included_section}\n\ncontent\n")

    with pytest.raises(ValueError, match=rf"## {section}"):
        parse_error_case(path)


@pytest.mark.parametrize("field", ["id", "title", "status"])
def test_missing_required_frontmatter_field_raises_value_error(
    tmp_path: Path, field: str
) -> None:
    fields = {"id": "err_test", "title": "Test error", "status": "resolved"}
    del fields[field]
    frontmatter = "".join(f"{key}: {value}\n" for key, value in fields.items())
    path = _write_case(
        tmp_path,
        "## Error\n\nbroken\n\n## Solution\n\nfixed\n",
        frontmatter=frontmatter,
    )

    with pytest.raises(ValueError, match=field):
        parse_error_case(path)


def test_all_sample_error_files_parse() -> None:
    cases = load_error_cases(ERRORS_DIR)

    assert len(cases) == 3
    assert {case.id for case in cases} == {
        "err_20260526_001",
        "err_20260526_002",
        "err_20260526_003",
    }
