from abc import abstractmethod
from typing import Protocol

from twaddle.parser.nodes import RootNode


# mostly just to avoid some type-hinting/circular import issues
class InterpreterDecoratorProtocol(Protocol):
    @abstractmethod
    def evaluate(self, root: RootNode) -> str:
        pass
