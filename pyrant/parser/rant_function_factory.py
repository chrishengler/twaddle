from collections import deque
from parser.rant_object import RantFunctionObject, RantTextObject
from lexer.rant_token import *
from rant_exceptions import *
from . import rant_parser_utils


def build(tokens: deque[RantToken]) -> RantFunctionObject:
    func = ""
    args = list()
    if not any(token.type == RantTokenType.RIGHT_SQUARE_BRACKET for token in tokens):
        raise RantParserException(
            "[FunctionFactory.build] Dictionary lookup has no closing angle bracket")

    # first thing must always be the opening square bracket:
    if tokens[0].type is not RantTokenType.LEFT_SQUARE_BRACKET:
        raise RantParserException(
            "[FunctionFactory.build] input does not begin with left angle bracket")
    tokens.popleft()

    # next thing must always be the function name, so it has to be text:
    if tokens[0].type is not RantTokenType.PLAIN_TEXT:
        raise RantParserException(
            "[FunctionFactory.build] opening angle bracket must be followed by dictionary name")

    # read the dictionary name and get rid of it so we can deal with the less fixed stuff
    func = tokens.popleft().value

    # if the function has arguments, there's a colon before the first:
    if tokens[0].type is RantTokenType.COLON:
        tokens.popleft()
        if tokens and tokens[0].type is not RantTokenType.RIGHT_SQUARE_BRACKET:
            args.append(collect_argument(tokens))
        else:
            raise RantParserException(
                "[FunctionFactory.build] colon with no argument")

    # now we have n (>= 0) arguments, each with a semicolon before it
    while len(tokens) > 0:
        token = tokens.popleft()
        match token.type:
            case RantTokenType.RIGHT_SQUARE_BRACKET:
                return RantFunctionObject(func, args)
            case RantTokenType.SEMICOLON:
                if tokens:
                    args.append(collect_argument(tokens))
                else:
                    raise RantParserException(
                        "[FunctionFactory.build] semicolon with no argument")
            case _:
                continue
    # if we reach here, something went wrong
    raise RantParserException(
        "[FunctionFactory.build] Error parsing dictionary lookup, probably an invalid character")


def collect_argument(tokens: deque[RantToken]) -> str:
    argument_ending_token_types = (
        RantTokenType.COLON, RantTokenType.SEMICOLON, RantTokenType.RIGHT_SQUARE_BRACKET)
    arg_as_list = deque()
    while tokens[0].type not in argument_ending_token_types:
        this_token = tokens.popleft()
        this_token_as_text = rant_parser_utils.to_plain_text_object(this_token)
        arg_as_list.append(this_token_as_text)
    return rant_parser_utils.merge_text_objects(arg_as_list).text

