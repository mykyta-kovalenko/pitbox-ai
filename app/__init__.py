"""Main Application Package"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configuration
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
ANALYTICS_MODEL = os.getenv("ANALYTICS_MODEL", "gpt-5-mini")
DEFAULT_TEMP = float(os.getenv("MODEL_TEMPERATURE", "0.1"))

# Simulator configuration
SIMULATOR_BASE_URL = os.getenv("SIMULATOR_BASE_URL", "http://127.0.0.1:8000")

# Knowledge base configuration
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "app/knowledge")
