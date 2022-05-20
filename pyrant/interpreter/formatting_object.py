from enum import Enum, auto


class FormattingStrategy(Enum):
    NONE = auto()
    UPPER = auto()
    LOWER = auto()
    SENTENCE = auto()
    TITLE = auto()


class FormattingObject:
    def __init__(self, previous):
        if previous is not None:
            self.previous = previous
            previous.next = self


class PlainText(FormattingObject):
    def __init__(self, previous: FormattingObject, text: str):
        FormattingObject.__init__(self, previous)
        self.text = text


class StrategyChange(FormattingObject):
    def __init__(self, previous: FormattingObject, strategy: FormattingStrategy):
        FormattingObject.__init__(self, previous)
        self.strategy = strategy


class IndefiniteArticle(FormattingObject):
    def __init__(self, previous: FormattingObject):
        FormattingObject.__init__(self, previous)
