from twaddle.compiler.compiler_objects import (
    BlockObject,
    DigitObject,
    FunctionObject,
    IndefiniteArticleObject,
    LookupObject,
    Object,
    RootObject,
    TextObject,
)
from twaddle.exceptions import TwaddleParserException
from twaddle.parser.twaddle_parser import Token, Transformer, v_args


class TwaddleTransformer(Transformer):
    def transform(self, tree):
        print("transforming")
        return super().transform(tree)

    # default
    def __default__(self, data, children, meta):
        print("transformer: default")
        raise TwaddleParserException(
            f"Unknown node at line {meta.line} column {meta.column}"
        )

    def __default_token__(self, token: Token):
        print("transformer: default token")
        raise TwaddleParserException(
            f"Unknown token at line {token.line}, column {token.column}"
        )

    # TERMINALS
    def NAME(self, token: Token) -> str:
        print("transformer: NAME")
        return TextObject(token.value)

    def TEXT(self, token: Token) -> str:
        print("transformer: TEXT")
        return TextObject(token.value)

    def ARG_TEXT(self, token: Token) -> str:
        print("transformer: ARG_TEXT")
        return TextObject(token.value)

    def LABEL_MODIFIER(self, children) -> str:
        print(f"label modifier: {children=}")
        return children[0]

    def TAG_MODIFIER(self, children) -> str:
        print(f"tag modifier: {children=}")
        return children[0]

    def SEMICOLON(self, _children) -> str:
        print("transformer: SEMICOLON")
        return TextObject(";")

    def PIPE(self, _children) -> str:
        print("transformer: PIPE")
        return TextObject("|")

    def ESCAPED_CHAR(self, children) -> str:
        print("transformer: ESCAPED CHAR")
        return children[0]

    # rules
    def start(self, children) -> RootObject:
        return children

    def element(self, children) -> Object:
        print(f"transformer: element {len(children)=}")
        return children[0]

    def choice_element(self, children) -> Object:
        print(f"transformer: choice element {len(children)=}")

    def arg_element(self, children) -> Object:
        print("transformer: arg_element")
        print(children)
        return children[0]

    def block(self, children) -> BlockObject:
        print("transformer: block")
        block = BlockObject(children)
        return block

    def choice(self, children) -> RootObject:
        print("transformer: choice")
        return children

    def function(self, children) -> FunctionObject:
        print("transformer: function")
        name = children[0].text
        args = children[1:]
        return FunctionObject(name, args)

    def arg(self, children) -> RootObject:
        print("transformer: arg")
        return children

    def lookup(self, children) -> LookupObject:
        print("transformer: lookup")
        dict_name = children[0]
        if len(children) == 0:
            return LookupObject(dict_name)
        modifiers = children[1:]
        print(f"{modifiers=}")
        return LookupObject(dict_name)

    def lookup_modifier(self, children) -> dict:
        print("transformer: lookup modifier")
        return children[0]

    def form(self, children) -> dict:
        print("transformer: form")
        return {"type": "form", "value": children[0]}

    @v_args(meta=True)
    def tag(self, meta, children) -> dict:
        print("transformer: tag")
        if len(children) == 1:
            return {"type": "positive_tag", "value": children[0]}
        elif children[0] == "!":
            return {"type": "negative_tag", "value": children[1]}
        else:
            raise TwaddleParserException(
                f"Unhandled label modifier '{children[0]} in label at line {meta.line}, column {meta.column}"
            )

    def tag_name(self, children) -> dict:
        print("transformer: tag name")
        return children[0]

    @v_args(meta=True)
    def label(self, meta, children) -> dict:
        print("transformer: label")
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
                raise TwaddleParserException(
                    f"Unhandled label modifier '{modifier} in label at line {meta.line}, column {meta.column}"
                )

    @v_args(meta=True)
    def escape(
        self, meta, children
    ) -> TextObject | IndefiniteArticleObject | DigitObject:
        print("transformer: escape")
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
            case "\\":
                return TextObject("\\")
            case ";":
                return TextObject(";")
            case _:
                raise TwaddleParserException(
                    f"invalid escape sequence \\{char} at line {meta.line}, column {meta.column}"
                )
