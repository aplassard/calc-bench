import os
import sys
from pathlib import Path

import pytest

# Ensure src is on path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from openai_client import setup_openai_client  # noqa: E402

MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-oss-120b")


@pytest.mark.integration
def test_hello_world():
    try:
        client = setup_openai_client()
    except EnvironmentError:
        pytest.skip("OPENAI_API_KEY not set; skipping integration test.")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "Say 'hello world'."}],
    )
    text = response.choices[0].message.content.lower()
    assert "hello" in text
