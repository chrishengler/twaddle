from types import WrapperDescriptorType
from collections import deque
import parser.rant_lookup_factory as LookupFactory
import parser.rant_block_factory as BlockFactory
import parser.rant_function_factory as FunctionFactory
from rant_exceptions import *
from lexer.rant_token import *
from parser.rant_object import *
from parser.rant_parser_utils import to_plain_text_object


def parse(tokens: deque[RantToken]) -> deque[RantObject]:
    parser_result = deque()
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
            case RantTokenType.LEFT_SQUARE_BRACKET:
                parser_result.append(FunctionFactory.build(tokens))
            case _:
                parser_result.append(to_plain_text_object(token))
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
