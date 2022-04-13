from collections import deque
from rant_object import RantFunctionObject
from rant_token import *
from rant_exceptions import *

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
        # argument must be text
        if tokens[0].type is RantTokenType.PLAIN_TEXT:
            args.append( str(tokens.popleft().value))
        else:
            raise RantParserException("[FunctionFactory.build] colon with no argument")

    # now we have n (>= 0) arguments, each with a semicolon before it
    while len(tokens) > 0:
        token = tokens.popleft()
        match token.type:
            case RantTokenType.RIGHT_SQUARE_BRACKET:
                return RantFunctionObject(func, args)
            case RantTokenType.SEMICOLON:
                if tokens[0].type is RantTokenType.PLAIN_TEXT:
                    args.append( str(tokens.popleft().value))
                else:
                    raise RantParserException("[FunctionFactory.build] colon with no argument")
            case _:
                continue
    # if we reach here, something went wrong
    raise RantParserException(
        "[FunctionFactory.build] Error parsing dictionary lookup, probably an invalid character")

