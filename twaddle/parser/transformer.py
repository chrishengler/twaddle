from dataclasses import dataclass

from twaddle.exceptions import TwaddleParserException
from twaddle.parser.nodes import (
    BlockNode,
    DigitNode,
    FunctionNode,
    IndefiniteArticleNode,
    LookupNode,
    Node,
    RegexNode,
    RootNode,
    TextNode,
)
from twaddle.parser.twaddle_parser import Token, Transformer


@dataclass
class FormModifier:
    value: TextNode


@dataclass
class TagModifier:
    value: TextNode
    negated: bool = False


@dataclass
class MatchLabelModifier:
    label: TextNode


@dataclass
class NegativeLabelModifier:
    label: TextNode


@dataclass
class RedefineLabelModifier:
    label: TextNode


LookupModifier = (
    FormModifier
    | TagModifier
    | MatchLabelModifier
    | NegativeLabelModifier
    | RedefineLabelModifier
)


class TwaddleTransformer(Transformer):
    # default
    def __default__(self, data, children, meta):
        raise TwaddleParserException(
            f"Unknown node at line {meta.line} column {meta.column}"
        )

    def __default_token__(self, token: Token):
        raise TwaddleParserException(
            f"Unknown token at line {token.line}, column {token.column}"
        )

    # TERMINALS
    def NAME(self, token: Token) -> TextNode:
        return TextNode(token.value)

    def TEXT(self, token: Token) -> TextNode:
        return TextNode(token.value)

    def ARG_TEXT(self, token: Token) -> TextNode:
        return TextNode(token.value)

    def LABEL_MODIFIER(self, children) -> TextNode:
        return children[0]

    def TAG_MODIFIER(self, children) -> TextNode:
        return children[0]

    def SEMICOLON(self, _children) -> TextNode:
        return TextNode(";")

    def PIPE(self, _children) -> TextNode:
        return TextNode("|")

    def ESCAPED_CHAR(self, children) -> str:
        return children[0]

    def FORWARD_SLASH(self, children) -> TextNode:
        return TextNode("/")

    def REGEX_BOUNDARY(self, children) -> TextNode:
        return TextNode("//")

    # rules
    def start(self, children) -> RootNode:
        return RootNode(children)

    def element(self, children) -> Node:
        return children[0]

    def choice_element(self, children) -> Node:
        return children[0]

    def arg_element(self, children) -> Node:
        return children[0]

    def block(self, children) -> BlockNode:
        choices = [c for c in children if isinstance(c, RootNode)]
        return BlockNode(choices)

    def choice(self, children) -> RootNode:
        return RootNode(children)

    def function(self, children) -> FunctionNode:
        return children[0]

    def standard_function(self, children) -> FunctionNode:
        name = children[0].text
        args = [c for c in children[1:] if isinstance(c, RootNode)]
        return FunctionNode(name, args)

    def arg(self, children) -> RootNode:
        return RootNode(children)

    def regex_pattern(self, children) -> str:
        parts = list[str]()
        for child in children:
            if isinstance(child, TextNode):
                parts.append(child.text)
            elif isinstance(child, str):
                parts.append(child)
            else:
                raise TwaddleParserException(
                    f"Regex pattern with unexpected child token type {type(child)}"
                )
        return "".join(parts)

    def old_regex(self, children) -> RegexNode:
        if len(children) < 4:
            raise TwaddleParserException(
                "Regex requires a pattern, a scope, and a replacement"
            )
        return RegexNode(regex=children[0], scope=children[1], replacement=children[3])

    def lookup(self, children) -> LookupNode:
        dict_name = children[0].text

        form = None
        positive_tags = set()
        negative_tags = set()
        positive_label = None
        negative_labels = set()
        redefine_labels = set()

        for mod in children[1:]:
            match mod:
                case FormModifier(value=v):
                    form = v.text
                case TagModifier(value=v, negated=False):
                    positive_tags.add(v.text)
                case TagModifier(value=v, negated=True):
                    negative_tags.add(v.text)
                case MatchLabelModifier(label=lbl):
                    positive_label = lbl.text
                case NegativeLabelModifier(label=lbl):
                    negative_labels.add(lbl.text)
                case RedefineLabelModifier(label=lbl):
                    redefine_labels.add(lbl.text)

        return LookupNode(
            dict_name,
            form,
            positive_tags,
            negative_tags,
            positive_label,
            negative_labels,
            redefine_labels,
        )

    def lookup_modifier(self, children) -> LookupModifier:
        return children[0]

    def form(self, children) -> FormModifier:
        return FormModifier(children[0])

    def tag(self, children) -> TagModifier:
        if len(children) == 1:
            return TagModifier(children[0])
        elif children[0] == "!":
            return TagModifier(children[1], negated=True)
        else:
            raise TwaddleParserException(f"Unhandled tag modifier '{children[0]}'")

    def label(
        self, children
    ) -> MatchLabelModifier | NegativeLabelModifier | RedefineLabelModifier:
        if len(children) == 1:
            return MatchLabelModifier(children[0])
        modifier = children[0]
        label = children[1]
        if modifier == "!":
            return NegativeLabelModifier(label)
        elif modifier == "^":
            return RedefineLabelModifier(label)
        else:
            raise TwaddleParserException(f"Unhandled label modifier '{modifier}'")

    def escape(self, children) -> TextNode | IndefiniteArticleNode | DigitNode:
        char = children[0]
        match char:
            case "a":
                return IndefiniteArticleNode(default_upper=False)
            case "A":
                return IndefiniteArticleNode(default_upper=True)
            case "d":
                return DigitNode()
            case "n":
                return TextNode("\n")
            case "t":
                return TextNode("\t")
            case "s":
                return TextNode(" ")
            case "\\" | ";" | "<" | ">" | "{" | "}" | "[" | "]" | "|" | ":":
                return TextNode(char)
            case _:
                raise TwaddleParserException(f"invalid escape sequence \\{char}")
