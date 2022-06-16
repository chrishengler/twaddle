from enum import Enum, auto
from typing import Type


class FormattingStrategy(Enum):
    NONE = auto()
    UPPER = auto()
    LOWER = auto()
    SENTENCE = auto()
    TITLE = auto()


class FormattingObject:
    def __init__(self, previous):
        self.previous = None
        if previous is not None:
            self.previous = previous
            previous.next = self
        self.next = None


class PlainText(FormattingObject):
    def __init__(self, previous: Type[FormattingObject], text: str):
        FormattingObject.__init__(self, previous)
        self.text = text


class StrategyChange(FormattingObject):
    def __init__(self, previous: Type[FormattingObject], strategy: FormattingStrategy):
        FormattingObject.__init__(self, previous)
        self.strategy = strategy


class IndefiniteArticle(FormattingObject):
    def __init__(
        self, previous: Type[FormattingObject], default_upper_case: bool = False
    ):
        FormattingObject.__init__(self, previous)
        self.default_upper = default_upper_case
