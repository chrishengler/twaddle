from types import WrapperDescriptorType
from collections import deque
import parser.rant_lookup_factory as LookupFactory
import parser.rant_block_factory as BlockFactory
from rant_exceptions import *
from lexer.rant_token import *
from parser.rant_object import *


def parse(tokens: deque[RantToken]) -> list[RantObject]:
    parser_result = list()
    i = 0

    while len(tokens) > 0:
        token = tokens[0]
        match token.type:
            case RantTokenType.PLAIN_TEXT:
                parser_result.append(RantTextObject(token.value))
                tokens.popleft()
            case RantTokenType.LEFT_ANGLE_BRACKET:
                parser_result.append(LookupFactory.build(tokens))
            case RantTokenType.LEFT_CURLY_BRACKET:
                parser_result.append(BlockFactory.build(tokens))

            # these symbols only have meaning in certain constructs
            # outside of those constructs, treat them as text
            case RantTokenType.EXCLAMATION_MARK:
                parser_result.append(RantTextObject('!'))
                tokens.popleft()
            case RantTokenType.COLON:
                parser_result.append(RantTextObject(':'))
                tokens.popleft()
            case RantTokenType.SEMICOLON:
                parser_result.append(RantTextObject(';'))
                tokens.popleft()
            case RantTokenType.PIPE:
                parser_result.append(RantTextObject('|'))
                tokens.popleft()
            case RantTokenType.HYPHEN:
                parser_result.append(RantTextObject('-'))
                tokens.popleft()
            case RantTokenType.DOUBLE_COLON:
                parser_result.append(RantTextObject('::'))
                tokens.popleft()
            case RantTokenType.SLASH:
                parser_result.append(RantTextObject('/'))
                tokens.popleft()
            case RantTokenType.DOT:
                parser_result.append(RantTextObject('.'))
                tokens.popleft()
            case RantTokenType.EQUALS:
                parser_result.append(RantTextObject('='))
                tokens.popleft()

            # unrecognised token type
            # should throw an error here once everything's ready
            case _:
                tokens.popleft()
    return parser_result


def consume_choice(tokens: deque[RantToken]) -> RantBlockObject:
    choices = deque()
    this_choice = deque()
    while len(tokens) > 0:
        token = tokens[0]
        tokens.popleft()
        match token.type:
            case RantTokenType.PIPE:
                choices.append(parse(this_choice))
                continue
            case RantTokenType.RIGHT_CURLY_BRACKET:
                choices.append(parse(this_choice))
                return RantBlockObject(choices)
            case _:
                this_choice.append(token)
                continue
    # something went wrong, fall over
    assert False
