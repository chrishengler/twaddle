from collections import deque
from rant_exceptions import RantParserException
from lexer.rant_token import *
from parser.rant_object import RantBlockObject
import parser.rant_parser as Parser


def build(tokens: deque[RantToken]) -> RantBlockObject:
    choices = list()
    this_choice = deque()
    if tokens[0].type is not RantTokenType.LEFT_CURLY_BRACKET:
        raise RantParserException(
            "[RantBlockFactory.build] block factory called without '{', this shouldn't happen!")
    tokens.popleft()

    """
    TODO:
    problem is here - this build function loops over the tokens, builds each choice, and parses the choices
    so when a choice contains a (nested) block, the tokens are already parsed and the parser doesn't know what to do

    maybe build a tree? 
    """
    while len(tokens) > 0:
        token = tokens.popleft()
        match token.type:
            case RantTokenType.PIPE:
                choices.append(Parser.parse(this_choice))
                continue
            case RantTokenType.RIGHT_CURLY_BRACKET:
                choices.append(Parser.parse(this_choice))
                return RantBlockObject(choices)
            case _:
                this_choice.append(token)
                continue
    # something went wrong, fall over
    raise RantParserException(
        "[RantBlockFactory.build] something went wrong, probably a missing '}'")
