from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class RootNode:
    contents: list["Node"]


@dataclass(frozen=True)
class TextNode:
    text: str


@dataclass(frozen=False)
class LookupNode:
    dictionary: str
    form: Optional[str] = None
    positive_tags: Optional[set[str]] = None
    negative_tags: Optional[set[str]] = None
    positive_label: Optional[str] = None
    negative_labels: Optional[set[str]] = None
    redefine_labels: Optional[set[str]] = None


@dataclass(frozen=True)
class BlockNode:
    choices: list[RootNode]


@dataclass(frozen=True)
class FunctionNode:
    func: str
    args: list[RootNode]


@dataclass(frozen=True)
class RegexNode:
    regex: str
    scope: RootNode
    replacement: RootNode


@dataclass(frozen=True)
class IndefiniteArticleNode:
    default_upper: bool


@dataclass(frozen=True)
class DigitNode:
    pass


Node = Union[
    RootNode,
    TextNode,
    LookupNode,
    BlockNode,
    FunctionNode,
    RegexNode,
    IndefiniteArticleNode,
    DigitNode,
]
