import os
import sys
from pathlib import Path

import pytest

# Disable tracing before importing the Agents SDK to avoid 401 telemetry errors.
os.environ.setdefault("OPENAI_AGENTS_DISABLE_TRACING", "true")

# Ensure src is on path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from agents import Agent  # noqa: E402
from openai_client import setup_agent_runner  # noqa: E402

MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-oss-120b")


@pytest.mark.integration
def test_agent_hello_world():
    runner, run_config = setup_agent_runner()
    agent = Agent(name="greeter", model=MODEL_NAME)
    result = runner.run_sync(agent, "Say 'hello world'.", run_config=run_config)
    text = result.final_output_as(str).lower()
    assert "hello" in text
