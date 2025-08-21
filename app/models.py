"""LLM Client Factory"""

import os
from functools import lru_cache
from typing import Optional

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


@lru_cache(maxsize=4)
def get_chat_model(
    model_name: Optional[str] = None, temperature: Optional[float] = None, **kwargs
) -> BaseChatModel:
    """Get a chat model instance with caching.

    Args:
        model_name: Model name to use (defaults to OPENAI_MODEL env var)
        temperature: Model temperature (defaults to MODEL_TEMPERATURE env var)
        **kwargs: Additional arguments passed to the model

    Returns:
        BaseChatModel: Configured chat model instance
    """
    model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    temperature = temperature or float(os.getenv("MODEL_TEMPERATURE", "0.1"))

    return ChatOpenAI(model=model_name, temperature=temperature, **kwargs)
