# AGENTS.md

## Project Overview

This project implements Debug Memory Vol.1: a local CLI tool that searches Markdown-based troubleshooting notes and returns solution candidates for similar software development errors.

## Scope

Implement only the Vol.1 internal system:
- Markdown error case parsing
- Error signature extraction
- Rule-based similar error search
- Solution candidate rendering
- CLI commands: search and ask
- Unit tests

Do not implement:
- Web UI
- LLM API integration
- Vector database
- Claude Skill integration
- Codex auto-fix workflow
- GitHub Issue integration

## Development Guidelines

- Keep the implementation simple and dependency-light.
- Prefer standard library modules where practical.
- Use PyYAML only if needed for frontmatter parsing.
- Use argparse for CLI unless there is a strong reason not to.
- Add tests for parser, signature extraction, search ranking, and answer rendering.
- The tool must work locally without external API calls.
- Search results must include evidence and reasons.
- Do not make the answer sound certain when it is based only on previous similar cases.
