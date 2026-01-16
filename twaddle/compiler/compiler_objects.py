from enum import Enum, auto
from typing import Optional


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
        self.contents = list[Object]()


class RootObject(Object):
    def __init__(self):
        Object.__init__(self, ObjectType.ROOT)
        self.contents = list[Object]()

    def __getitem__(self, n: int) -> Object:
        return self.contents[n]

    def __len__(self) -> int:
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
        form: Optional[str] = None,
        positive_tags: Optional[set[str]] = None,
        negative_tags: Optional[set[str]] = None,
        positive_label: Optional[str] = None,
        negative_labels: Optional[set[str]] = None,
        redefine_labels: Optional[set[str]] = None,
        strict_mode: bool = False,
    ):
        Object.__init__(self, ObjectType.LOOKUP)
        self.dictionary = dictionary
        self.form = form
        self.positive_tags = positive_tags or set[str]()
        self.negative_tags = negative_tags or set[str]()
        self.positive_label = positive_label or str()
        self.negative_labels = negative_labels or set[str]()
        self.redefine_labels = redefine_labels or set[str]()
        self.strict_mode = strict_mode


class BlockObject(Object):
    def __init__(self, choices: list[RootObject]):
        Object.__init__(self, ObjectType.BLOCK)
        self.choices = choices

    def __getitem__(self, n: int) -> list[Object]:
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
