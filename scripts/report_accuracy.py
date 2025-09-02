"""Report accuracy of math agents on a dataset using gpt-oss-20b."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable, Dict, Any

# Ensure src/ on the path for direct execution
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import math_agent

Row = Dict[str, Any]


def _load_dataset(path: Path) -> list[Row]:
    """Load JSONL dataset from ``path``."""
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


def _accuracy(rows: list[Row], evaluator: Callable[[Row, str], str], model: str) -> tuple[int, int]:
    """Return number of correct predictions and total rows.

    Any exception raised by ``evaluator`` is surfaced with row context so
    authentication or connection issues don't silently pass as perfect
    accuracy.
    """
    correct = 0
    for idx, row in enumerate(rows, 1):
        try:
            if evaluator(row, model) == row["solution"]:
                correct += 1
        except Exception as exc:  # pragma: no cover - defensive
            raise RuntimeError(f"evaluation failed for row {idx}: {row}") from exc
    return correct, len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report accuracy for math agents")
    parser.add_argument("--dataset", default=str(Path(__file__).resolve().parents[1] / "datasets" / "sample.jsonl"))
    parser.add_argument("--model", default="gpt-oss-20b")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    rows = _load_dataset(dataset_path)

    print(f"Model: {args.model}")
    print(f"Dataset: {dataset_path}")

    for evaluator in (math_agent.evaluate_equation, math_agent.evaluate_equation_with_tools):
        correct, total = _accuracy(rows, evaluator, args.model)
        accuracy = correct / total if total else 0.0
        print(f"{evaluator.__name__}: {correct}/{total} correct ({accuracy:.0%})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
