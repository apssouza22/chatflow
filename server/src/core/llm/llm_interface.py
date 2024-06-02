from abc import abstractmethod, ABC
from typing import List


class LLMInterface(ABC):
    """Interface for LLMs."""

    @abstractmethod
    def predict(self, prompts: List[dict]):
        pass

    @abstractmethod
    def create_embeddings(self, inputs: List[str]) -> List[list]:
        pass
