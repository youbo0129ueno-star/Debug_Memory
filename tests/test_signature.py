from debug_memory.signature import extract_signature


def test_extracts_python_missing_package_signature() -> None:
    signature = extract_signature(
        "ModuleNotFoundError: No module named 'dotenv'\n"
        "pip install python-dotenv"
    )

    assert signature.exception_names == ["ModuleNotFoundError"]
    assert signature.quoted_terms == ["dotenv"]
    assert signature.package_names == ["dotenv", "python-dotenv"]
    assert signature.commands == ["pip install python-dotenv"]


def test_extracts_react_type_error_and_npm_command() -> None:
    signature = extract_signature(
        "TypeError: Cannot read properties of undefined in react\n"
        "npm install foo"
    )

    assert signature.exception_names == ["TypeError"]
    assert signature.package_names == ["foo"]
    assert signature.commands == ["npm install foo"]
    assert "properties" in signature.keywords


def test_deduplicates_features_case_insensitively_preserving_first_form() -> None:
    signature = extract_signature(
        "TypeError TypeError typeerror\n"
        "No module named 'dotenv'; No module named \"DOTENV\"\n"
        "pip install python-dotenv\nPIP install PYTHON-DOTENV"
    )

    assert signature.exception_names == ["TypeError"]
    assert signature.quoted_terms == ["dotenv"]
    assert signature.package_names == ["dotenv", "python-dotenv"]
    assert signature.commands == ["pip install python-dotenv"]
