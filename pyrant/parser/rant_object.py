from enum import Enum, auto
from typing import Type

import lexer.rant_lexer as RantLexer


class RantObjectType(Enum):
    TEXT = auto()      # plain text
    LOOKUP = auto()    # something looked up from a dictionary
    BLOCK = auto()     # choice from multiple options
    FUNCTION = auto()  # call to a rant function


class RantObject:
    def __init__(self, t: RantObjectType):
        self.type = t


class RantTextObject(RantObject):
    def __init__(self, text: str):
        RantObject.__init__(self, RantObjectType.TEXT)
        self.text = text


class RantLookupObject(RantObject):
    def __init__(self, dictionary: str, form: str = "", category: str = "", labels: list[tuple[str, bool]] = []):
        RantObject.__init__(self, RantObjectType.LOOKUP)
        self.dictionary = dictionary
        self.form = form
        self.category = category
        self.labels = labels


class RantBlockObject(RantObject):
    def __init__(self, choices: list[RantObject]):
        RantObject.__init__(self, RantObjectType.BLOCK)
        self.choices = choices


class RantFunctionObject(RantObject):
    def __init__(self, func: str, args: list[str]):
        RantObject.__init__(self, RantObjectType.FUNCTION)
        self.func = func
        self.args = args
