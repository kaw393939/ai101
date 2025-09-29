"""
Pytest configuration and fixtures.
"""

import pytest
import os
import tempfile
from pathlib import Path


@pytest.fixture
def temp_config_dir():
    """Create a temporary configuration directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / "config"
        config_dir.mkdir()
        yield config_dir


@pytest.fixture
def sample_ai_config():
    """Sample AI configuration for testing."""
    return {
        "providers": {
            "groq": {
                "api_key_env": "GROQ_API_KEY",
                "base_url": "https://api.groq.com/openai/v1",
                "models": ["llama3-70b-8192", "llama3-8b-8192"],
                "default_model": "llama3-70b-8192"
            },
            "openai": {
                "api_key_env": "OPENAI_API_KEY",
                "base_url": "https://api.openai.com/v1",
                "models": ["gpt-3.5-turbo", "gpt-4"],
                "default_model": "gpt-3.5-turbo"
            }
        },
        "default_provider": "groq",
        "default_model": "llama3-70b-8192",
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 1000
        },
        "prompts": {
            "system": {
                "default": "You are a helpful AI assistant."
            },
            "user": {
                "coding": "Help with coding tasks."
            }
        }
    }


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    monkeypatch.setenv("GROQ_API_KEY", "test_groq_key")
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_anthropic_key")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DEBUG", "True")


@pytest.fixture
def logs_dir():
    """Ensure logs directory exists for testing."""
    logs_path = Path("logs")
    logs_path.mkdir(exist_ok=True)
    yield logs_path