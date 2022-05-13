from enum import Enum, auto
from rant_exceptions import RantInterpreterException


class FormattingStrategy(Enum):
    NONE = auto()
    UPPER = auto()
    LOWER = auto()
    SENTENCE = auto()
    TITLE = auto()


class Formatter:
    def __init__(self):
        self.sentence = str()
        self.strategy = FormattingStrategy.NONE

    def reset(self):
        self.sentence = str()

    def append(self, text: str):
        match self.strategy:
            case FormattingStrategy.NONE:
                self.sentence += text
            case FormattingStrategy.UPPER:
                self.sentence += text.upper()
            case FormattingStrategy.LOWER:
                self.sentence += text.lower()
            case FormattingStrategy.SENTENCE:
                self.sentence += self.apply_sentence_case(text)
            case FormattingStrategy.TITLE:
                self.sentence += self.apply_title_case(text)
            case _:
                raise RantInterpreterException(
                    f"[Formatter.append] no handling defined for {self.strategy}")

    def get(self) -> str:
        return self.sentence

    def set_strategy(self, strategy: FormattingStrategy):
        self.strategy = strategy

    def apply_sentence_case(self, text: str) -> str:
        result = str()
        sentence_start = False
        if self.sentence == "" or self.sentence.strip()[-1] in ".!?":
            sentence_start = True
        for char in text:
            if sentence_start:
                result += char.upper()
            else:
                result += char.lower()
            if not char.isspace():
                sentence_start = char in ".!?"
        return result

    def apply_title_case(self, text: str) -> str:
        result = str()
        word_start = False
        if not self.sentence or self.sentence[-1].isspace():
            word_start = True
        for char in text:
            if word_start:
                result += char.upper()
            else:
                result += char.lower()
            word_start = True if char.isspace() else False
        return result
