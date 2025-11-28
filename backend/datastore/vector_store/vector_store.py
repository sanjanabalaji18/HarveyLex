from abc import ABC, abstractmethod
from typing import Any, List, Dict
import numpy as np
 

class VectorStore(ABC):
    """
    Abstract base vector store.
    Concrete implementations must override add() and search().
    """

    @abstractmethod
    async def add(self, text: str, vector: np.ndarray, metadata: Dict[str, Any]):
        pass

    @abstractmethod
    async def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        pass

