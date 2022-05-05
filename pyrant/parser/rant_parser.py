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
    result = deque()

    while len(tokens) > 0:
        token = tokens[0]
        match token.type:
            case RantTokenType.PLAIN_TEXT:
                result.append(RantTextObject(token.value))
                tokens.popleft()
            case RantTokenType.LEFT_ANGLE_BRACKET:
                result.append(LookupFactory.build(tokens))
            case RantTokenType.LEFT_CURLY_BRACKET:
                result.append(BlockFactory.build(tokens))
            case RantTokenType.LEFT_SQUARE_BRACKET:
                result.append(FunctionFactory.build(tokens))
            case _:
                result.append(to_plain_text_object(token))
                tokens.popleft()

    return result
