from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, raw_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a raw JSON payload from the websocket and returns a normalized dictionary.
        """
        pass
