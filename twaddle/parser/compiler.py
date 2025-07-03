from collections import deque
from enum import Enum, auto

from twaddle.exceptions import TwaddleParserException
from twaddle.lexer.lexer import lex
from twaddle.lexer.lexer_tokens import Token, TokenType

from .compiler_objects import (
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
from .compiler_utils import get_text_for_object, to_plain_text_object


class CompilerContext(Enum):
    ROOT = auto()
    FUNCTION = auto()
    LOOKUP = auto()
    BLOCK = auto()
    REGEX = auto()


class CompilerContextStack:
    def __init__(self):
        self.stack = deque[CompilerContext]()
        self.stack.append(CompilerContext.ROOT)

    def current_context(self):
        return self.stack[-1]

    def add_context(self, context: CompilerContext):
        self.stack.append(context)

    def remove_context(self, context: CompilerContext):
        if self.current_context() is not context:
            raise TwaddleParserException(
                f"[CompilerContextStack::remove_context] tried to remove {context.name} "
                f"but current context is {self.stack[-1].name}"
            )
        self.stack.pop()


class Compiler:
    def __init__(self):
        self.context = CompilerContextStack()

    def compile(self, sentence: str) -> RootObject:
        result = self.parse_root(lex(sentence))
        if self.context.current_context() is not CompilerContext.ROOT:
            raise TwaddleParserException(
                f"[RantCompiler::compile] reached end while still in {self.context.current_context().name} context"
            )
        return result

    def parse_root(self, tokens: deque[Token]) -> RootObject:
        result = RootObject()
        while tokens:
            context = self.context.current_context()
            token = tokens[0]
            match token.type:
                case TokenType.PLAIN_TEXT:
                    result.append(TextObject(token.value))
                    tokens.popleft()
                case TokenType.LEFT_ANGLE_BRACKET:
                    self.context.add_context(CompilerContext.LOOKUP)
                    result.append(self.parse_lookup(tokens))
                case TokenType.LEFT_CURLY_BRACKET:
                    self.context.add_context(CompilerContext.BLOCK)
                    result.append(self.parse_block(tokens))
                case TokenType.LEFT_SQUARE_BRACKET:
                    if len(tokens) and tokens[1].type == TokenType.REGEX:
                        self.context.add_context(CompilerContext.REGEX)
                        result.append(self.parse_regex(tokens))
                    else:
                        self.context.add_context(CompilerContext.FUNCTION)
                        result.append(self.parse_function(tokens))
                case TokenType.PIPE:
                    if context is CompilerContext.BLOCK:
                        return result
                    else:
                        result.append(to_plain_text_object(token))
                        tokens.popleft()
                case TokenType.RIGHT_CURLY_BRACKET:
                    if context is CompilerContext.BLOCK:
                        return result
                case TokenType.COLON:
                    if context is CompilerContext.FUNCTION:
                        return result
                    if context is CompilerContext.REGEX:
                        return result
                    else:
                        result.append(to_plain_text_object(token))
                        tokens.popleft()
                case TokenType.SEMICOLON:
                    if context is CompilerContext.FUNCTION:
                        return result
                    if context is CompilerContext.REGEX:
                        return result
                    else:
                        result.append(to_plain_text_object(token))
                        tokens.popleft()
                case TokenType.RIGHT_SQUARE_BRACKET:
                    if context is CompilerContext.FUNCTION:
                        return result
                    if context is CompilerContext.REGEX:
                        return result
                case TokenType.RIGHT_ANGLE_BRACKET:
                    if context is CompilerContext.LOOKUP:
                        return result
                case TokenType.LOWER_INDEFINITE_ARTICLE:
                    result.append(IndefiniteArticleObject())
                    tokens.popleft()
                case TokenType.UPPER_INDEFINITE_ARTICLE:
                    result.append(IndefiniteArticleObject(default_upper_case=True))
                    tokens.popleft()
                case TokenType.DIGIT:
                    result.append(DigitObject())
                    tokens.popleft()
                # more special cases to handle here later, just convert to text for now
                case _:
                    result.append(to_plain_text_object(token))
                    tokens.popleft()
        return result

    def parse_lookup(self, tokens: deque[Token]) -> Object:
        form = None
        positive_tags = set[str]()
        negative_tags = set[str]()
        positive_label = None
        negative_labels = set[str]()

        # first thing must always be the opening angle bracket:
        if tokens[0].type is not TokenType.LEFT_ANGLE_BRACKET:
            raise TwaddleParserException(
                "[Compiler.parse_block] input does not begin with left angle bracket"
            )
        tokens.popleft()

        # next thing must always be the dictionary name, so it has to be text:
        if tokens[0].type is not TokenType.PLAIN_TEXT:
            raise TwaddleParserException(
                "[Compiler.parse_block] opening angle bracket must be followed by dictionary name"
            )

        # read the dictionary name and get rid of it so we can deal with the less fixed stuff
        dictionary = tokens.popleft().value

        while len(tokens) > 0:
            token = tokens.popleft()
            match token.type:
                case TokenType.RIGHT_ANGLE_BRACKET:
                    self.context.remove_context(CompilerContext.LOOKUP)
                    return LookupObject(
                        dictionary,
                        form,
                        positive_tags,
                        negative_tags,
                        positive_label,
                        negative_labels,
                    )
                case TokenType.DOT:
                    if tokens[0].type is not TokenType.PLAIN_TEXT:
                        raise TwaddleParserException(
                            "[Compiler.parse_block] dot must be followed by form"
                        )
                    form = tokens.popleft().value
                    continue
                case TokenType.HYPHEN:
                    positive = True
                    if tokens[0].type is TokenType.EXCLAMATION_MARK:
                        tokens.popleft()
                        positive = False
                    if tokens[0].type is not TokenType.PLAIN_TEXT:
                        raise TwaddleParserException(
                            "[Compiler.parse_block] hyphen must be followed by category"
                        )
                    category = tokens.popleft().value
                    if positive:
                        positive_tags.add(category)
                    else:
                        negative_tags.add(category)
                    continue
                case TokenType.DOUBLE_COLON:
                    if tokens[0].type is TokenType.EQUALS:
                        tokens.popleft()
                        if len(tokens) > 0 and tokens[0].type is TokenType.PLAIN_TEXT:
                            positive_label = tokens.popleft().value
                        else:
                            raise TwaddleParserException(
                                "[Compiler.parse_block] no valid definition for match"
                            )
                    elif tokens[0].type is TokenType.EXCLAMATION_MARK:
                        tokens.popleft()
                        if (
                            len(tokens) >= 2
                            and tokens[0].type is TokenType.EQUALS
                            and tokens[1].type is TokenType.PLAIN_TEXT
                        ):
                            # get rid of the equals
                            tokens.popleft()
                            # get label name
                            negative_labels.add(tokens.popleft().value)
                        else:
                            raise TwaddleParserException(
                                "[Compiler.parse_block] no valid definition for anti-match"
                            )
                case _:
                    continue
        # if we reach here, something went wrong
        raise TwaddleParserException(
            "[Compiler.parse_block] Error parsing dictionary lookup, probably an invalid character"
        )

    def parse_block(self, tokens: deque[Token]) -> BlockObject:
        choices = list()
        this_choice = RootObject()
        if tokens[0].type is not TokenType.LEFT_CURLY_BRACKET:
            raise TwaddleParserException(
                "[Compiler.parse_block] block factory called without '{', this shouldn't happen!"
            )
        tokens.popleft()
        while len(tokens) > 0:
            token = tokens[0]
            match token.type:
                case TokenType.PIPE:
                    tokens.popleft()
                    choices.append(this_choice)
                    continue
                case TokenType.RIGHT_CURLY_BRACKET:
                    tokens.popleft()
                    choices.append(this_choice)
                    self.context.remove_context(CompilerContext.BLOCK)
                    return BlockObject(choices)
                case _:
                    this_choice = self.parse_root(tokens)
        # something went wrong, fall over
        raise TwaddleParserException(
            "[Compiler.parse_block] something went wrong, probably a missing '}'"
        )

    # noinspection GrazieInspection
    def parse_function(self, tokens: deque[Token]) -> FunctionObject:
        args = list()

        # first thing must always be the opening square bracket:
        if tokens[0].type is not TokenType.LEFT_SQUARE_BRACKET:
            raise TwaddleParserException(
                "[Compiler.parse_function] input does not begin with left angle bracket"
            )
        tokens.popleft()

        # next thing must always be the function name, so it has to be text:
        if tokens[0].type is not TokenType.PLAIN_TEXT:
            raise TwaddleParserException(
                "[Compiler.parse_function] expected function name"
            )

        # read the dictionary name and get rid of it so we can deal with the less fixed stuff
        func = tokens.popleft().value

        while len(tokens) > 0:
            token = tokens.popleft()
            match token.type:
                case TokenType.COLON:
                    args.append(self.parse_root(tokens))
                    continue
                case TokenType.SEMICOLON:
                    args.append(self.parse_root(tokens))
                    continue
                case TokenType.RIGHT_SQUARE_BRACKET:
                    self.context.remove_context(CompilerContext.FUNCTION)
                    return FunctionObject(func, args)
                case _:
                    continue
        # if we reach here, something went wrong
        raise TwaddleParserException(
            "[Compiler.parse_function] Error parsing function, probably an invalid character or missing closing bracket"
        )

    def parse_regex(self, tokens: deque[Token]) -> RegexObject:
        regex = ""
        scope = RootObject()
        replacement = RootObject()

        # first thing must always be the opening square bracket:
        if tokens[0].type is not TokenType.LEFT_SQUARE_BRACKET:
            raise TwaddleParserException(
                "[Compiler.parse_regex] input does not begin with left angle bracket"
            )
        tokens.popleft()

        # next thing must always be the regex
        if tokens[0].type is not TokenType.REGEX:
            raise TwaddleParserException(
                "[Compiler.parse_regex] expected function name"
            )
        tokens.popleft()

        while len(tokens) and tokens[0].type is not TokenType.REGEX:
            token = tokens.popleft()
            match token.type:
                case TokenType.PLAIN_TEXT:
                    regex += token.value
                case _:
                    regex += get_text_for_object(token)

        if len(tokens) == 0:
            raise TwaddleParserException(
                "[Compiler.parse_regex] reached end of input without finding end of regex"
            )
        tokens.popleft()

        while len(tokens):
            token = tokens.popleft()
            match token.type:
                case TokenType.COLON:
                    scope = self.parse_root(tokens)
                case TokenType.SEMICOLON:
                    replacement = self.parse_root(tokens)
                case TokenType.RIGHT_SQUARE_BRACKET:
                    self.context.remove_context(CompilerContext.REGEX)
                    return RegexObject(regex, scope, replacement)
                case _:
                    continue
        # if we reach here, something went wrong
        raise TwaddleParserException(
            "[Compiler.parse_regex] Error parsing regex, probably an invalid character or missing closing bracket"
        )
