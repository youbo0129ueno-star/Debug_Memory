from pathlib import Path

from debug_memory.parser import load_error_cases
from debug_memory.search import search_similar_cases


ERRORS_DIR = Path(__file__).parent.parent / "memory" / "errors"


def _cases():
    return load_error_cases(ERRORS_DIR)


def test_dotenv_query_ranks_python_dotenv_first() -> None:
    results = search_similar_cases(
        "Python ModuleNotFoundError: No module named 'dotenv'", _cases()
    )

    assert results[0].case.id == "err_20260526_001"


def test_cors_query_ranks_fastapi_cors_first() -> None:
    results = search_similar_cases(
        "CORS blocked request in a Python FastAPI application", _cases()
    )

    assert results[0].case.id == "err_20260526_002"


def test_react_undefined_map_query_ranks_react_case_first() -> None:
    results = search_similar_cases(
        "React TypeError: Cannot read properties of undefined (reading 'map')",
        _cases(),
    )

    assert results[0].case.id == "err_20260526_003"


def test_resolved_case_receives_status_bonus() -> None:
    result = search_similar_cases("ModuleNotFoundError: 'dotenv'", _cases())[0]

    assert "status bonus: resolved" in result.reasons


def test_top_result_includes_match_reasons() -> None:
    result = search_similar_cases("FastAPI CORS policy blocked request", _cases())[0]

    assert result.reasons
