"""
Configuration module for OT Mentor AI system.

Handles model configuration, API key management, and application settings.
"""

import os
from dataclasses import dataclass
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ModelConfig:
    """Configuration for a specific LLM model."""
    technical_name: str  # LangChain model identifier
    provider_api: Literal["google"]  # API provider
    ui_name: str  # Display name in UI
    ui_locked: bool = True  # Whether model selection is locked in UI


# Available model configurations
# Currently locked to Gemini Flash 2.5 as per technical design
AVAILABLE_MODELS = [
    ModelConfig(
        technical_name="gemini-2.5-flash",
        provider_api="google",
        ui_name="Gemini 2.5 Flash",
        ui_locked=True
    )
]

# Default model (first in list)
DEFAULT_MODEL = AVAILABLE_MODELS[0]


@dataclass
class AppConfig:
    """Application-wide configuration."""

    # Model settings
    model_config: ModelConfig = None

    # Google API configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")

    # Embedding model
    embedding_model: str = "models/gemini-embedding-001"  # Gemini Embedding 001

    # RAG settings
    top_k_scenarios: int = 2  # Number of scenarios to retrieve
    chroma_db_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db")
    chroma_collection_name: str = "ot_scenarios"

    # Session persistence
    sessions_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sessions")

    # Phase transition criteria
    critical_fields_count: int = 5  # Must have all 5 critical fields
    additional_fields_count: int = 7  # Plus at least 7 additional fields
    min_total_fields: int = 12  # Total minimum (5 + 7)

    def __post_init__(self):
        """Set default model config if not provided."""
        if self.model_config is None:
            self.model_config = DEFAULT_MODEL

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        return True


# Global config instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get the global configuration instance."""
    return config


def set_model(model_config: ModelConfig) -> None:
    """Update the active model configuration."""
    global config
    config.model_config = model_config
