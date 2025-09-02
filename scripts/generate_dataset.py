#!/usr/bin/env python3
"""Generate a math accuracy dataset.

This script creates arithmetic equations and variants to test whether
systems can distinguish correct calculations from incorrect ones.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import random
from typing import List, Dict

OPERATIONS = ['+', '-', '*']


def random_number() -> int:
    """Return a random integer with 3 to 5 digits."""
    digits = random.randint(3, 5)
    start = 10 ** (digits - 1)
    end = 10 ** digits - 1
    return random.randint(start, end)


def mutate_digit(value: int) -> int:
    """Change a single digit in ``value`` by +1 (modulo 10)."""
    sign = -1 if value < 0 else 1
    s = list(str(abs(value)))
    idx = random.randrange(len(s))
    digit = int(s[idx])
    s[idx] = str((digit + 1) % 10)
    return sign * int("".join(s))


def eval_expression(a: int, b: int, op: str) -> int:
    """Evaluate ``a op b`` for supported operations."""
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    raise ValueError(f"Unknown operation: {op}")


def generate_entries(count: int, seed: int = 42) -> List[Dict[str, object]]:
    """Generate dataset entries.

    Each original equation is accompanied by two incorrect variants:
    one with a mutated result and one with a mutated operand.
    """
    random.seed(seed)
    entries: List[Dict[str, object]] = []
    for i in range(count):
        op = OPERATIONS[i % len(OPERATIONS)]
        a = random_number()
        b = random_number()
        correct = eval_expression(a, b, op)

        base = {
            "first": a,
            "second": b,
            "operation": op,
            "result": correct,
            "equation": f"{a} {op} {b} = {correct}",
            "solution": "correct",
        }
        entries.append(base)

        wrong_result = mutate_digit(correct)
        entries.append(
            {
                "first": a,
                "second": b,
                "operation": op,
                "result": wrong_result,
                "equation": f"{a} {op} {b} = {wrong_result}",
                "solution": "incorrect",
            }
        )

        if random.choice([True, False]):
            new_a = mutate_digit(a)
            entries.append(
                {
                    "first": new_a,
                    "second": b,
                    "operation": op,
                    "result": correct,
                    "equation": f"{new_a} {op} {b} = {correct}",
                    "solution": "incorrect",
                }
            )
        else:
            new_b = mutate_digit(b)
            entries.append(
                {
                    "first": a,
                    "second": new_b,
                    "operation": op,
                    "result": correct,
                    "equation": f"{a} {op} {new_b} = {correct}",
                    "solution": "incorrect",
                }
            )

    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate math accuracy dataset.")
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("datasets/math_accuracy.jsonl"),
        help="Where to write the dataset.",
    )
    parser.add_argument(
        "--size", type=int, default=1000, help="Number of base problems to generate."
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility."
    )
    args = parser.parse_args()

    entries = generate_entries(args.size, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for item in entries:
            json.dump(item, f)
            f.write("\n")


if __name__ == "__main__":
    main()
