"""Math agent utilities for evaluating arithmetic equations."""

from __future__ import annotations

import asyncio
from typing import Any, Dict

from agents import Agent
from agents.tool import function_tool

from openai_client import setup_agent_runner


async def _run_agent(agent: Agent, prompt: str, model_name: str) -> str:
    """Execute ``agent`` against ``prompt`` using ``model_name``.

    Parameters
    ----------
    agent:
        The :class:`agents.Agent` to execute.
    prompt:
        Question or instruction for the agent.
    model_name:
        Name of the model to use.

    Returns
    -------
    str
        The agent's final output lowercased.
    """
    runner, run_config = setup_agent_runner()
    run_config.model = model_name
    result = await runner.run(agent, prompt, run_config=run_config)
    output = str(result.final_output).strip().lower()
    return output.rstrip(".!")


def evaluate_equation(row: Dict[str, Any], model_name: str) -> str:
    """Determine whether an equation is correct.

    Parameters
    ----------
    row:
        Dataset record containing an ``equation`` field.
    model_name:
        Identifier of the model to query.

    Returns
    -------
    str
        ``"correct"`` if the equation holds or ``"incorrect"`` otherwise.

    Notes
    -----
    This simple version of the agent uses no tools and relies solely on the
    model's reasoning capabilities.
    """
    agent = Agent(
        name="math-judge",
        instructions=(
            "You are given an arithmetic equation. Respond with 'correct' if the "
            "equation is true or 'incorrect' if it is false."
        ),
    )
    return asyncio.run(_run_agent(agent, row["equation"], model_name))


@function_tool
def addition(a: int, b: int) -> int:
    """Return the sum of ``a`` and ``b``."""
    return a + b


@function_tool
def subtraction(a: int, b: int) -> int:
    """Return the result of ``a`` minus ``b``."""
    return a - b


@function_tool
def multiplication(a: int, b: int) -> int:
    """Return the product of ``a`` and ``b``."""
    return a * b


def evaluate_equation_with_tools(row: Dict[str, Any], model_name: str) -> str:
    """Determine whether an equation is correct using math tools.

    Parameters
    ----------
    row:
        Dataset record containing an ``equation`` field.
    model_name:
        Identifier of the model to query.

    Returns
    -------
    str
        ``"correct"`` if the equation holds or ``"incorrect"`` otherwise.
    """
    agent = Agent(
        name="math-judge-tools",
        instructions=(
            "You are given an arithmetic equation. Use the available math tools "
            "to compute results. Respond with 'correct' if the equation is true "
            "or 'incorrect' if it is false."
        ),
        tools=[addition, subtraction, multiplication],
    )
    return asyncio.run(_run_agent(agent, row["equation"], model_name))
