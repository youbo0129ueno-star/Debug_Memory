from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .parser import load_error_cases
from .rag import build_answer
from .render import render_search_results
from .search import search_similar_cases


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text", required=True, help="Error message or log to search for.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Maximum number of similar cases to return (default: 3).",
    )
    parser.add_argument(
        "--errors-dir",
        default="memory/errors",
        help="Directory containing Markdown error cases (default: memory/errors).",
    )


def _resolve_errors_dir(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="debug-memory")
    subcommands = parser.add_subparsers(dest="command", required=True)

    search_parser = subcommands.add_parser("search", help="List similar error cases.")
    _add_common_args(search_parser)

    ask_parser = subcommands.add_parser("ask", help="Render a solution candidate.")
    _add_common_args(ask_parser)

    args = parser.parse_args(argv)
    errors_dir = _resolve_errors_dir(args.errors_dir)
    cases = load_error_cases(errors_dir)
    if not cases:
        print(f"no cases found at {errors_dir}", file=sys.stderr)
        return 2

    results = search_similar_cases(args.text, cases, top_k=args.top_k)
    if args.command == "search":
        print(render_search_results(results))
    else:
        print(build_answer(args.text, results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
