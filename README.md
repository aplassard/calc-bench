# calc-bench

Can LLMs do math? Do tools help?

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency
management. Install the dependencies with:

```sh
uv sync
```

## OpenAI client

`src/openai_client.py` exposes utilities for working with the OpenAI API:

- `setup_openai_client` builds an `OpenAI` client. It checks for
  `OPENAI_API_KEY` and optionally `OPENAI_BASE_URL` in the environment, loading
  a `.env` file when either is missing.
- `setup_agent_runner` wires up an `AgentRunner` from the
  [openai-agents](https://pypi.org/project/openai-agents/) SDK. It respects the
  same environment variables, disables tracing by default, and can target
  alternate gateways like OpenRouter.

## Tests

Integration tests demonstrate both the raw client and the Agent SDK via the
`gpt-oss-120b` model by default:

- `tests/test_integration.py` exercises the chat completions API.
- `tests/test_agent_sdk.py` drives an `Agent`.

Run all tests with:

```sh
uv run pytest
```

The model name can be customized through the `MODEL_NAME` environment variable,
and an `OPENAI_BASE_URL` may be supplied to target alternative gateways such as
OpenRouter. The GitHub Actions workflow passes these variables along with an
`OPENAI_API_KEY` secret to exercise the integration tests.

## Development setup

This project uses [uv](https://github.com/astral-sh/uv) to manage Python
and run scripts. After installing uv, commands can be executed in an
isolated environment using `uv run`.

## Dataset generation

`scripts/generate_dataset.py` creates arithmetic equations for testing
math accuracy. Each of the 1,000 base problems cycles between addition,
subtraction, and multiplication with 3–5 digit operands. For every
problem a correct equation is produced along with two incorrect
variants.

Generate the full dataset:

```bash
uv run scripts/generate_dataset.py
```

The script writes a JSONL file to `datasets/math_accuracy.jsonl`, which
is ignored by git. A small example dataset is checked in at
`datasets/sample.jsonl`.
