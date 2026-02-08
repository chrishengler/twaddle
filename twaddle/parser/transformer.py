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
    def NAME(self, token: Token) -> TextObject:
        print("transformer: NAME")
        return TextObject(token.value)

    def TEXT(self, token: Token) -> TextObject:
        print("transformer: TEXT")
        return TextObject(token.value)

    def ARG_TEXT(self, token: Token) -> TextObject:
        print("transformer: ARG_TEXT")
        return TextObject(token.value)

    def LABEL_MODIFIER(self, children) -> TextObject:
        print(f"label modifier: {children=}")
        return children[0]

    def TAG_MODIFIER(self, children) -> TextObject:
        print(f"tag modifier: {children=}")
        return children[0]

    def SEMICOLON(self, _children) -> TextObject:
        print("transformer: SEMICOLON")
        return TextObject(";")

    def PIPE(self, _children) -> TextObject:
        print("transformer: PIPE")
        return TextObject("|")

    def ESCAPED_CHAR(self, children) -> str:
        print("transformer: ESCAPED CHAR")
        return children[0]

    def FORWARD_SLASH(self, children) -> TextObject:
        print("transformer: FORWARD_SLASH")
        return TextObject("/")

    def REGEX_BOUNDARY(self, children) -> TextObject:
        print("transformer: REGEX_BOUNDARY")
        return TextObject("//")

    # rules
    def start(self, children) -> RootObject:
        root = RootObject()
        for child in children:
            root.append(child)
        return root

    def element(self, children) -> Object:
        print(f"transformer: element {len(children)=}")
        return children[0]

    def choice_element(self, children) -> Object:
        print(f"transformer: choice element {len(children)=}")
        return children[0]

    def arg_element(self, children) -> Object:
        print("transformer: arg_element")
        print(children)
        return children[0]

    def block(self, children) -> BlockObject:
        print("transformer: block")
        choices = [c for c in children if isinstance(c, RootObject)]
        return BlockObject(choices)

    def choice(self, children) -> RootObject:
        print("transformer: choice")
        root = RootObject()
        for child in children:
            root.append(child)
        return root

    def function(self, children) -> FunctionObject:
        print("transformer: function")
        return children[0]

    def standard_function(self, children) -> FunctionObject:
        print("transformer: standard function")
        name = children[0].text
        args = [c for c in children[1:] if isinstance(c, RootObject)]
        return FunctionObject(name, args)

    def arg(self, children) -> RootObject:
        print("transformer: arg")
        root = RootObject()
        for child in children:
            root.append(child)
        return root

    @v_args(meta=True)
    def regex_pattern(self, meta, children) -> str:
        print("transformer: regex_pattern")
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
        print("transformer: old_regex")
        for child in children:
            print(f"{child} ({type(child)})")
        if len(children) < 4:
            raise TwaddleParserException(
                "Regex requires a pattern, a scope, and a replacement"
            )
        # TODO: fill actual values once I confirm that this is being parsed correctly in the first place
        return RegexObject(children[0], children[1], children[3])

    def lookup(self, children) -> LookupObject:
        print("transformer: lookup")
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
            case "\\" | ";" | "<" | ">" | "{" | "}" | "[" | "]" | "|" | ":":
                return TextObject(char)
            case _:
                print(meta)
                raise TwaddleParserException(
                    f"invalid escape sequence \\{char} at line {meta.line}, column {meta.column}"
                )
