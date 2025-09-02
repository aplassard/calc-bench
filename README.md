# calc-bench

Can LLMs do math? Do tools help?

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
