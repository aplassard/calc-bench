import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

if TYPE_CHECKING:
    # Only used for type hints to avoid importing the agents package at module import
    from agents.models.multi_provider import MultiProvider
    from agents.run import AgentRunner, RunConfig


def setup_openai_client() -> OpenAI:
    """Create an OpenAI client using environment variables.

    If ``OPENAI_API_KEY`` is missing, attempts to load variables from a ``.env``
    file. When ``OPENAI_BASE_URL`` is provided, the client connects to that
    endpoint.
    """
    if "OPENAI_API_KEY" not in os.environ or "OPENAI_BASE_URL" not in os.environ:
        load_dotenv()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def setup_agent_runner() -> "tuple[AgentRunner, RunConfig]":
    """Configure an :class:`AgentRunner` aware of custom OpenAI endpoints.

    Tracing is disabled by default so the Agents SDK doesn't attempt to send
    telemetry to the OpenAI backend when using alternative providers.
    """

    # Disable built-in tracing unless explicitly re-enabled by the caller.
    os.environ.setdefault("OPENAI_AGENTS_DISABLE_TRACING", "true")

    # Import here so the environment variable above takes effect before the
    # Agents SDK initializes its tracing provider.
    from agents.models.multi_provider import MultiProvider
    from agents.run import AgentRunner, RunConfig

    client = setup_openai_client()

    async_client = AsyncOpenAI(api_key=client.api_key, base_url=client.base_url)
    provider = MultiProvider(openai_client=async_client, openai_use_responses=False)
    run_config = RunConfig(model_provider=provider)
    return AgentRunner(), run_config
