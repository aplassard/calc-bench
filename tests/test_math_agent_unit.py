import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

# Ensure src on path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import math_agent  # noqa: E402


def test_evaluate_equation_no_tools(monkeypatch):
    row = {"equation": "2 + 2 = 4"}

    captured = {}

    async def fake_run(agent, prompt, run_config=None):
        captured["agent"] = agent
        captured["prompt"] = prompt
        return SimpleNamespace(final_output="correct")

    def fake_setup_runner():
        return SimpleNamespace(run=fake_run), SimpleNamespace(model=None)

    monkeypatch.setattr(math_agent, "setup_agent_runner", fake_setup_runner)

    result = math_agent.evaluate_equation(row, "gpt-test")
    assert result == "correct"
    assert captured["agent"].tools == []


def test_evaluate_equation_with_tools(monkeypatch):
    row = {"equation": "2 + 2 = 5"}

    captured = {}

    async def fake_run(agent, prompt, run_config=None):
        captured["agent"] = agent
        captured["prompt"] = prompt
        return SimpleNamespace(final_output="incorrect")

    def fake_setup_runner():
        return SimpleNamespace(run=fake_run), SimpleNamespace(model=None)

    monkeypatch.setattr(math_agent, "setup_agent_runner", fake_setup_runner)

    result = math_agent.evaluate_equation_with_tools(row, "gpt-test")
    assert result == "incorrect"
    assert len(captured["agent"].tools) == 3
