"""State Schemas"""

from typing import Any, Dict, List, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated


class PitBoxState(TypedDict):
    """Main state schema for NASCAR Pit Box AI.

    Attributes:
        messages: Conversation history with safe message accumulation
        race_context: Current race information (lap, flag status, etc.)
    """

    messages: Annotated[List[BaseMessage], add_messages]
    race_context: Optional[Dict[str, Any]]
