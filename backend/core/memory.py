from collections import defaultdict
from typing import List, Dict, Any


class SessionMemory:
    """
    A simple in-memory store for session-specific conversation history.
    This is not suitable for production but is perfect for this course.
    """

    def __init__(self):
        # Stores chat history per session_id
        self._history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves the history for a given session."""
        return self._history.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str):
        """Adds a new message to the session's history."""
        self._history[session_id].append({"role": role, "content": content})

    def clear_history(self, session_id: str):
        """Clears the history for a specific session."""
        if session_id in self._history:
            del self._history[session_id]


# Singleton instance to be used across the application
memory_service = SessionMemory()
