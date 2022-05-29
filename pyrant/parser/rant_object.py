from enum import Enum, auto
from typing import Type

import lexer.rant_lexer as RantLexer


class RantObjectType(Enum):
    ROOT = auto()
    TEXT = auto()               # plain text
    LOOKUP = auto()             # something looked up from a dictionary
    BLOCK = auto()              # choice from multiple options
    FUNCTION = auto()           # call to a rant function
    INDEFINITE_ARTICLE = auto()  # a/an, depending what follows
    DIGIT = auto()              # a random digit 0-9
    REGEX = auto()              # a regex


class RantObject:
    def __init__(self, t: RantObjectType):
        self.type = t


class RantRootObject:
    def __init__(self):
        RantObject.__init__(self, RantObjectType.ROOT)
        self.contents = list[RantObject]()

    def __getitem__(self, n: int):
        return self.contents[n]

    def __len__(self):
        return len(self.contents)

    def append(self, new_content: RantObject):
        self.contents.append(new_content)


class RantTextObject(RantObject):
    def __init__(self, text: str):
        RantObject.__init__(self, RantObjectType.TEXT)
        self.text = text


class RantLookupObject(RantObject):
    def __init__(self, dictionary: str, form: str = None,
                 positive_tags: set[str] = {}, negative_tags: set[str] = {},
                 positive_label: str = None, negative_labels: set[str] = {}):
        RantObject.__init__(self, RantObjectType.LOOKUP)
        self.dictionary = dictionary
        self.form = form
        self.positive_tags = positive_tags
        self.negative_tags = negative_tags
        self.positive_label = positive_label
        self.negative_labels = negative_labels


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


class RantRegexObject(RantObject):
    def __init__(self, regex: str, scope: RantRootObject, replacement: RantRootObject):
        RantObject.__init__(self, RantObjectType.REGEX)
        self.regex = regex
        self.scope = scope
        self.replacement = replacement


class RantIndefiniteArticleObject(RantObject):
    def __init__(self, default_upper_case: bool = False):
        RantObject.__init__(self, RantObjectType.INDEFINITE_ARTICLE)
        self.default_upper = default_upper_case


class RantDigitObject(RantObject):
    def __init__(self):
        RantObject.__init__(self, RantObjectType.DIGIT)
