from enum import Enum, auto
from lexer.rant_token import *
from lexer.rant_lexer import lex
from .rant_object import *
from rant_exceptions import RantParserException
from collections import deque
from .rant_parser_utils import *


class CompilerContext(Enum):
    ROOT = auto()
    FUNCTION = auto()
    LOOKUP = auto()
    BLOCK = auto()


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
            raise RantParserException(
                f"[CompilerContextStack::remove_context] tried to remove {context.name} but current context is {self.stack[-1].name}")
        self.stack.pop()


class RantCompiler:
    def __init__(self):
        self.context = CompilerContextStack()

    def compile(self, sentence: str) -> RantRootObject:
        result = self.parse_root(RantLexer.lex(sentence))
        if self.context.current_context() is not CompilerContext.ROOT:
            raise RantParserException(
                "[RantCompiler::compile] reached end while still in {self.context.current_context().name} context")
        return result

    def parse_root(self, tokens: deque[RantToken]) -> RantRootObject:
        result = RantRootObject()
        while tokens:
            token = tokens[0]
            match token.type:
                case RantTokenType.PLAIN_TEXT:
                    result.append(RantTextObject(token.value))
                    tokens.popleft()
                case RantTokenType.LEFT_ANGLE_BRACKET:
                    self.context.add_context(CompilerContext.LOOKUP)
                    result.append(self.parse_lookup(tokens))
                case RantTokenType.LEFT_CURLY_BRACKET:
                    self.context.add_context(CompilerContext.BLOCK)
                    result.append(self.parse_block(tokens))
                case RantTokenType.LEFT_SQUARE_BRACKET:
                    self.context.add_context(CompilerContext.FUNCTION)
                    result.append(self.parse_function(tokens))
                case RantTokenType.PIPE:
                    if self.context.current_context() is CompilerContext.BLOCK:
                        return result
                    else:
                        result.append(to_plain_text_object(token))
                        tokens.popleft()
                case RantTokenType.RIGHT_CURLY_BRACKET:
                    if self.context.current_context() is CompilerContext.BLOCK:
                        return result
                case RantTokenType.COLON:
                    if self.context.current_context() is CompilerContext.FUNCTION:
                        return result
                    else:
                        result.append(to_plain_text_object(token))
                        tokens.popleft()
                case RantTokenType.SEMICOLON:
                    if self.context.current_context() is CompilerContext.FUNCTION:
                        return result
                    else:
                        result.append(to_plain_text_object(token))
                        tokens.popleft()
                case RantTokenType.RIGHT_SQUARE_BRACKET:
                    if self.context.current_context() is CompilerContext.FUNCTION:
                        return result
                case RantTokenType.RIGHT_ANGLE_BRACKET:
                    if self.context.current_context() is CompilerContext.LOOKUP:
                        return result
                case RantTokenType.LOWER_INDEFINITE_ARTICLE:
                    result.append(RantIndefiniteArticleObject())
                    tokens.popleft()
                case RantTokenType.UPPER_INDEFINITE_ARTICLE:
                    result.append(RantIndefiniteArticleObject(
                        default_upper_case=True))
                    tokens.popleft()
                # more special cases to handle here later, just convert to text for now
                case _:
                    result.append(to_plain_text_object(token))
                    tokens.popleft()
        return result

    def parse_lookup(self, tokens: deque[RantToken]) -> deque[RantObject]:
        dictionary = None
        form = None
        positive_tags = set[str]()
        negative_tags = set[str]()
        positive_label = None
        negative_labels = set[str]()

        # first thing must always be the opening angle bracket:
        if tokens[0].type is not RantTokenType.LEFT_ANGLE_BRACKET:
            raise RantParserException(
                "[Compiler.parse_block] input does not begin with left angle bracket")
        tokens.popleft()

        # next thing must always be the dictionary name, so it has to be text:
        if tokens[0].type is not RantTokenType.PLAIN_TEXT:
            raise RantParserException(
                "[Compiler.parse_block] opening angle bracket must be followed by dictionary name")

        # read the dictionary name and get rid of it so we can deal with the less fixed stuff
        dictionary = tokens.popleft().value

        while len(tokens) > 0:
            token = tokens.popleft()
            match token.type:
                case RantTokenType.RIGHT_ANGLE_BRACKET:
                    self.context.remove_context(CompilerContext.LOOKUP)
                    return RantLookupObject(dictionary, form, positive_tags, negative_tags, positive_label, negative_labels)
                case RantTokenType.DOT:
                    if tokens[0].type is not RantTokenType.PLAIN_TEXT:
                        raise RantParserException(
                            "[Compiler.parse_block] dot must be followed by form")
                    form = tokens.popleft().value
                    continue
                case RantTokenType.HYPHEN:
                    positive = True
                    if tokens[0].type is RantTokenType.EXCLAMATION_MARK:
                        tokens.popleft()
                        positive = False
                    if tokens[0].type is not RantTokenType.PLAIN_TEXT:
                        raise RantParserException(
                            "[Compiler.parse_block] hyphen must be followed by category")
                    category = tokens.popleft().value
                    if positive:
                        positive_tags.add(category)
                    else:
                        negative_tags.add(category)
                    continue
                case RantTokenType.DOUBLE_COLON:
                    if tokens[0].type is RantTokenType.EQUALS:
                        tokens.popleft()
                        if len(tokens) > 0 and tokens[0].type is RantTokenType.PLAIN_TEXT:
                            positive_label = tokens.popleft().value
                        else:
                            raise RantParserException(
                                "[Compiler.parse_block] no valid definition for match")
                    elif tokens[0].type is RantTokenType.EXCLAMATION_MARK:
                        tokens.popleft()
                        if len(tokens) >= 2 and tokens[0].type is RantTokenType.EQUALS and tokens[1].type is RantTokenType.PLAIN_TEXT:
                            # get rid of the equals
                            tokens.popleft()
                            # get label name
                            negative_labels.add(tokens.popleft().value)
                        else:
                            raise RantParserException(
                                "[Compiler.parse_block] no valid definition for anti-match")
                case _:
                    continue
        # if we reach here, something went wrong
        raise RantParserException(
            "[Compiler.parse_block] Error parsing dictionary lookup, probably an invalid character")

    def parse_block(self, tokens: deque[RantToken]) -> RantBlockObject:
        choices = list()
        this_choice = deque()
        if tokens[0].type is not RantTokenType.LEFT_CURLY_BRACKET:
            raise RantParserException(
                "[Compiler.parse_block] block factory called without '{', this shouldn't happen!")
        tokens.popleft()
        while len(tokens) > 0:
            token = tokens[0]
            match token.type:
                case RantTokenType.PIPE:
                    tokens.popleft()
                    choices.append(this_choice)
                    continue
                case RantTokenType.RIGHT_CURLY_BRACKET:
                    tokens.popleft()
                    choices.append(this_choice)
                    self.context.remove_context(CompilerContext.BLOCK)
                    return RantBlockObject(choices)
                case _:
                    this_choice = self.parse_root(tokens)
        # something went wrong, fall over
        raise RantParserException(
            "[Compiler.parse_block] something went wrong, probably a missing '}'")

    def parse_function(self, tokens: deque[RantToken]) -> RantFunctionObject:
        func = ""
        args = list()

        # first thing must always be the opening square bracket:
        if tokens[0].type is not RantTokenType.LEFT_SQUARE_BRACKET:
            raise RantParserException(
                "[Compiler.parse_function] input does not begin with left angle bracket")
        tokens.popleft()

        # next thing must always be the function name, so it has to be text:
        if tokens[0].type is not RantTokenType.PLAIN_TEXT:
            raise RantParserException(
                "[Compiler.parse_function] expected function name")

        # read the dictionary name and get rid of it so we can deal with the less fixed stuff
        func = tokens.popleft().value

        while len(tokens) > 0:
            token = tokens.popleft()
            match token.type:
                case RantTokenType.COLON:
                    args.append(self.parse_root(tokens))
                    continue
                case RantTokenType.SEMICOLON:
                    args.append(self.parse_root(tokens))
                    continue
                case RantTokenType.RIGHT_SQUARE_BRACKET:
                    self.context.remove_context(CompilerContext.FUNCTION)
                    return RantFunctionObject(func, args)
                case _:
                    continue
        # if we reach here, something went wrong
        raise RantParserException(
            "[Compiler.parse_function] Error parsing dictionary lookup, probably an invalid character")
