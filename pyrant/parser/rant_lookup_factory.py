from collections import deque
from rant_exceptions import RantParserException
from lexer.rant_token import *
from parser.rant_object import RantLookupObject


def build(tokens: deque[RantToken]) -> RantLookupObject:
    dictionary = None
    form = ""
    category = ""
    labels = list() 
    if not any(token.type == RantTokenType.RIGHT_ANGLE_BRACKET for token in tokens):
        raise RantParserException(
            "[RantLookupFactory.build] Dictionary lookup has no closing angle bracket")

    # first thing must always be the opening angle bracket:
    if tokens[0].type is not RantTokenType.LEFT_ANGLE_BRACKET:
        raise RantParserException(
            "[RantLookupFactory.build] input does not begin with left angle bracket")
    tokens.popleft()

    # next thing must always be the dictionary name, so it has to be text:
    if tokens[0].type is not RantTokenType.PLAIN_TEXT:
        raise RantParserException(
            "[RantLookupFactory.build] opening angle bracket must be followed by dictionary name")

    # read the dictionary name and get rid of it so we can deal with the less fixed stuff
    dictionary = tokens.popleft().value

    while len(tokens) > 0:
        token = tokens.popleft()
        match token.type:
            case RantTokenType.RIGHT_ANGLE_BRACKET:
                return RantLookupObject(dictionary, form, category, labels)
                continue
            case RantTokenType.DOT:
                if tokens[0].type is not RantTokenType.PLAIN_TEXT:
                    raise RantParserException(
                        "[RantLookupFactory.build] dot must be followed by form")
                form = tokens.popleft().value
                continue
            case RantTokenType.HYPHEN:
                if tokens[0].type is not RantTokenType.PLAIN_TEXT:
                    raise RantParserException(
                        "[RantLookupFactory.build] hyphen must be followed by category")
                category = tokens.popleft().value
                continue
            case RantTokenType.DOUBLE_COLON:
                if tokens[0].type is RantTokenType.EQUALS:
                    tokens.popleft()
                    if len(tokens) > 0 and tokens[0].type is RantTokenType.PLAIN_TEXT:
                        labels.append((tokens.popleft().value, True))
                    else:
                        raise RantParserException("[RantLookupFactory.build] no valid definition for match")
                elif tokens[0].type is RantTokenType.EXCLAMATION_MARK:
                    tokens.popleft()
                    if len(tokens) >= 2 and tokens[0].type is RantTokenType.EQUALS and tokens[1].type is RantTokenType.PLAIN_TEXT:
                        # get rid of the equals
                        tokens.popleft()
                        # get label name
                        labels.append((tokens.popleft().value, False))
                    else:
                        raise RantParserException("[LookupBuilder.build] no valid definition for anti-match")
            case _:
                continue
    # if we reach here, something went wrong
    raise RantParserException(
        "[RantLookupFactory.build] Error parsing dictionary lookup, probably an invalid character")

