from enum import Enum, auto
from typing import Type


class ObjectType(Enum):
    ROOT = auto()
    TEXT = auto()  # plain text
    LOOKUP = auto()  # something looked up from a dictionary
    BLOCK = auto()  # choice from multiple options
    FUNCTION = auto()  # call to a rant function
    INDEFINITE_ARTICLE = auto()  # a/an, depending what follows
    DIGIT = auto()  # a random digit 0-9
    REGEX = auto()  # a regex


class Object:
    def __init__(self, t: ObjectType):
        self.type = t


class RootObject(Object):
    def __init__(self):
        Object.__init__(self, ObjectType.ROOT)
        self.contents = list[Object]()

    def __getitem__(self, n: int):
        return self.contents[n]

    def __len__(self):
        return len(self.contents)

    def append(self, new_content: Object):
        self.contents.append(new_content)


class TextObject(Object):
    def __init__(self, text: str):
        Object.__init__(self, ObjectType.TEXT)
        self.text = text


class LookupObject(Object):
    def __init__(
        self,
        dictionary: str,
        form: str = None,
        positive_tags: set[str] = None,
        negative_tags: set[str] = None,
        positive_label: str = None,
        negative_labels: set[str] = None,
    ):
        Object.__init__(self, ObjectType.LOOKUP)
        self.dictionary = dictionary
        self.form = form
        self.positive_tags = positive_tags
        self.negative_tags = negative_tags
        self.positive_label = positive_label
        self.negative_labels = negative_labels


class BlockObject(Object):
    def __init__(self, choices: list[Type[RootObject]]):
        Object.__init__(self, ObjectType.BLOCK)
        self.choices = choices

    def __getitem__(self, n: int):
        return self.choices[n].contents

    def __len__(self):
        return len(self.choices)


class FunctionObject(Object):
    def __init__(self, func: str, args: list[RootObject]):
        Object.__init__(self, ObjectType.FUNCTION)
        self.func = func
        self.args = args


class RegexObject(Object):
    def __init__(self, regex: str, scope: RootObject, replacement: RootObject):
        Object.__init__(self, ObjectType.REGEX)
        self.regex = regex
        self.scope = scope
        self.replacement = replacement


class IndefiniteArticleObject(Object):
    def __init__(self, default_upper_case: bool = False):
        Object.__init__(self, ObjectType.INDEFINITE_ARTICLE)
        self.default_upper = default_upper_case


class DigitObject(Object):
    def __init__(self):
        Object.__init__(self, ObjectType.DIGIT)
