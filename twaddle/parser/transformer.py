from twaddle.compiler.compiler_objects import (
    BlockObject,
    DigitObject,
    FunctionObject,
    IndefiniteArticleObject,
    LookupObject,
    Object,
    RegexObject,
    RootObject,
    TextObject,
)
from twaddle.exceptions import TwaddleParserException
from twaddle.parser.twaddle_parser import Token, Transformer


class TwaddleTransformer(Transformer):
    def transform(self, tree):
        return super().transform(tree)

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
    def NAME(self, token: Token) -> TextObject:
        return TextObject(token.value)

    def TEXT(self, token: Token) -> TextObject:
        return TextObject(token.value)

    def ARG_TEXT(self, token: Token) -> TextObject:
        return TextObject(token.value)

    def LABEL_MODIFIER(self, children) -> TextObject:
        return children[0]

    def TAG_MODIFIER(self, children) -> TextObject:
        return children[0]

    def SEMICOLON(self, _children) -> TextObject:
        return TextObject(";")

    def PIPE(self, _children) -> TextObject:
        return TextObject("|")

    def ESCAPED_CHAR(self, children) -> str:
        return children[0]

    def FORWARD_SLASH(self, children) -> TextObject:
        return TextObject("/")

    def REGEX_BOUNDARY(self, children) -> TextObject:
        return TextObject("//")

    # rules
    def start(self, children) -> RootObject:
        root = RootObject()
        for child in children:
            root.append(child)
        return root

    def element(self, children) -> Object:
        return children[0]

    def choice_element(self, children) -> Object:
        return children[0]

    def arg_element(self, children) -> Object:
        return children[0]

    def block(self, children) -> BlockObject:
        choices = [c for c in children if isinstance(c, RootObject)]
        return BlockObject(choices)

    def choice(self, children) -> RootObject:
        root = RootObject()
        for child in children:
            root.append(child)
        return root

    def function(self, children) -> FunctionObject:
        return children[0]

    def standard_function(self, children) -> FunctionObject:
        name = children[0].text
        args = [c for c in children[1:] if isinstance(c, RootObject)]
        return FunctionObject(name, args)

    def arg(self, children) -> RootObject:
        root = RootObject()
        for child in children:
            root.append(child)
        return root

    def regex_pattern(self, children) -> str:
        parts = list[str]()
        for child in children:
            if isinstance(child, TextObject):
                parts.append(child.text)
            elif isinstance(child, str):
                parts.append(child)
            else:
                raise TwaddleParserException(
                    f"Regex pattern with unexpected child token type {type(child)}"
                )
        return "".join(parts)

    def old_regex(self, children) -> RegexObject:
        if len(children) < 4:
            raise TwaddleParserException(
                "Regex requires a pattern, a scope, and a replacement"
            )
        return RegexObject(children[0], children[1], children[3])

    def lookup(self, children) -> LookupObject:
        dict_name = children[0].text

        form = None
        positive_tags = set()
        negative_tags = set()
        positive_label = None
        negative_labels = set()
        redefine_labels = set()

        for mod in children[1:]:
            match mod.get("type"):
                case "form":
                    form = mod["value"].text
                case "positive_tag":
                    positive_tags.add(mod["value"].text)
                case "negative_tag":
                    negative_tags.add(mod["value"].text)
                case "match_label":
                    positive_label = mod["label"].text
                case "negative_label":
                    negative_labels.add(mod["label"].text)
                case "force_define_label":
                    redefine_labels.add(mod["label"].text)

        return LookupObject(
            dict_name,
            form,
            positive_tags,
            negative_tags,
            positive_label,
            negative_labels,
            redefine_labels,
        )

    def lookup_modifier(self, children) -> dict:
        return children[0]

    def form(self, children) -> dict:
        return {"type": "form", "value": children[0]}

    def tag(self, children) -> dict:
        if len(children) == 1:
            return {"type": "positive_tag", "value": children[0]}
        elif children[0] == "!":
            return {"type": "negative_tag", "value": children[1]}
        else:
            raise TwaddleParserException(f"Unhandled tag modifier '{children[0]}'")

    def label(self, children) -> dict:
        if len(children) == 1:
            return {"type": "match_label", "label": children[0]}
        else:
            modifier = children[0]
            label = children[1]
            if modifier == "!":
                return {"type": "negative_label", "label": label}
            elif modifier == "^":
                return {"type": "force_define_label", "label": label}
            else:
                raise TwaddleParserException(f"Unhandled label modifier '{modifier}'")

    def escape(self, children) -> TextObject | IndefiniteArticleObject | DigitObject:
        char = children[0]
        match char:
            case "a":
                return IndefiniteArticleObject(default_upper_case=False)
            case "A":
                return IndefiniteArticleObject(default_upper_case=True)
            case "d":
                return DigitObject()
            case "n":
                return TextObject("\n")
            case "t":
                return TextObject("\t")
            case "s":
                return TextObject(" ")
            case "\\" | ";" | "<" | ">" | "{" | "}" | "[" | "]" | "|" | ":":
                return TextObject(char)
            case _:
                raise TwaddleParserException(f"invalid escape sequence \\{char}")
