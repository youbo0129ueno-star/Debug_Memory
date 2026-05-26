from pathlib import Path

from debug_memory.parser import load_error_cases
from debug_memory.rag import build_answer
from debug_memory.search import search_similar_cases


ERRORS_DIR = Path(__file__).parent.parent / "memory" / "errors"
DOTENV_QUERY = "Python ModuleNotFoundError: No module named 'dotenv'"


def _cases():
    return load_error_cases(ERRORS_DIR)


def test_dotenv_answer_contains_solution_from_resolved_case() -> None:
    answer = build_answer(DOTENV_QUERY, search_similar_cases(DOTENV_QUERY, _cases()))

    assert "pip install python-dotenv" in answer


def test_dotenv_answer_contains_evidence() -> None:
    answer = build_answer(DOTENV_QUERY, search_similar_cases(DOTENV_QUERY, _cases()))

    assert "Evidence:" in answer
    assert "2026-05-26_python-dotenv.md" in answer


def test_empty_search_answer_reports_no_resolved_candidate() -> None:
    query = "UnrecordedError: entirely unknown failure"
    results = search_similar_cases(query, _cases(), top_k=0)
    answer = build_answer(query, results)

    assert "No resolved solution candidate found." in answer
    assert "Similar unresolved cases:\n(none)" in answer
