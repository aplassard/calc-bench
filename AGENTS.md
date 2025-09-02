
# Developer Instructions

- Source code lives in `src/` and tests in `tests/`.
- Use `uv` for all Python commands and dependency management.
- Run the test suite with `uv run pytest`.
- The `setup_openai_client` function reads `OPENAI_API_KEY` and optional
  `OPENAI_BASE_URL` from the environment and loads a `.env` file when either is
  missing.
- `setup_agent_runner` builds an Agent SDK `AgentRunner` honoring the same
  environment variables and disables tracing by default so custom gateways do
  not trigger OpenAI telemetry errors.
- Integration tests default to the `gpt-oss-120b` model but honor a
  `MODEL_NAME` environment variable.

- Run Python tasks using `uv run` to ensure a managed environment.
- The dataset generator lives in `scripts/generate_dataset.py`.
- Files under `datasets/` are ignored by git except for
  `datasets/sample.jsonl`, which illustrates the format.
- Prefer type hints and docstrings for new Python code.
