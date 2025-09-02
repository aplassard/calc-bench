import json
import os
import sys
from pathlib import Path

import pytest

# Ensure src path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import math_agent  # noqa: E402

MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-oss-120b")
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "sample.jsonl"


@pytest.mark.integration
@pytest.mark.parametrize("evaluator", [math_agent.evaluate_equation, math_agent.evaluate_equation_with_tools])
def test_sample_dataset(evaluator):
    with open(DATASET_PATH, "r", encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh]

    for row in rows:
        assert evaluator(row, MODEL_NAME) == row["solution"]
