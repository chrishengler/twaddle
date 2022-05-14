from enum import Enum, auto
from typing import Type

import lexer.rant_lexer as RantLexer


class RantObjectType(Enum):
    ROOT = auto()
    TEXT = auto()      # plain text
    LOOKUP = auto()    # something looked up from a dictionary
    BLOCK = auto()     # choice from multiple options
    FUNCTION = auto()  # call to a rant function


class RantObject:
    def __init__(self, t: RantObjectType):
        self.type = t


class RantRootObject:
    def __init__(self):
        RantObject.__init__(self, RantObjectType.ROOT)
        self.contents = list[RantObject]()

    def __getitem__(self, n: int):
        return self.contents[n]

    def append(self, new_content: RantObject):
        self.contents.append(new_content)


class RantTextObject(RantObject):
    def __init__(self, text: str):
        RantObject.__init__(self, RantObjectType.TEXT)
        self.text = text


class RantLookupObject(RantObject):
    def __init__(self, dictionary: str, form: str = None, category: str = None, labels: list[tuple[str, bool]] = []):
        RantObject.__init__(self, RantObjectType.LOOKUP)
        self.dictionary = dictionary
        self.form = form
        self.category = category
        self.labels = labels


class RantBlockObject(RantObject):
    def __init__(self, choices: list[RantObject]):
        RantObject.__init__(self, RantObjectType.BLOCK)
        self.choices = choices

    def __getitem__(self, n: int):
        return self.choices[n].contents

    def __len__(self):
        return len(self.choices)

class RantFunctionObject(RantObject):
    def __init__(self, func: str, args: list[str]):
        RantObject.__init__(self, RantObjectType.FUNCTION)
        self.func = func
        self.args = args
