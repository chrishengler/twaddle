from rant_exceptions import RantParserException
from rant_token import *
from rant_object import RantLookupObject

def build(tokens: list[RantToken]) -> RantLookupObject:
    dictionary = None
    form = ""
    category = ""
    label = ""
    if not any(token.type == RantTokenType.RIGHT_ANGLE_BRACKET for token in tokens):
       raise RantParserException("[LookupBuilder::build] Dictionary lookup has no closing angle bracket")

    # first thing must always be the opening angle bracket:
    if tokens[0].type is not RantTokenType.LEFT_ANGLE_BRACKET:
       raise RantParserException("[LookupBuilder::build] input does not begin with left angle bracket")
    tokens.pop(0)

    # next thing must always be the dictionary name, so it has to be text:
    if tokens[0].type is not RantTokenType.PLAIN_TEXT:
        raise RantParserException("[LookupBuilder::build] opening angle bracket must be followed by dictionary name")

    # read the dictionary name and get rid of it so we can deal with the less fixed stuff
    dictionary = tokens[0].value
    tokens.pop(0)

    while len(tokens) > 0:
        token = tokens[0]
        tokens.pop(0)
        match token.type:
            case RantTokenType.RIGHT_ANGLE_BRACKET:
                return RantLookupObject(dictionary, form, category, label)
                continue
            case RantTokenType.DOT:
                if tokens[0].type is not RantTokenType.PLAIN_TEXT:
                   raise RantParserException("[LookupBuilder::build] dot must be followed by form")
                form = tokens[0].value
                tokens.pop(0)
                continue
            case RantTokenType.HYPHEN:
                # TODO: as above
                if tokens[0].type is not RantTokenType.PLAIN_TEXT:
                   raise RantParserException("[LookupBuilder::build] hyphen must be followed by category")
                category = tokens[0].value
                tokens.pop(0)
                continue
            case _:
                continue
    # if we reach here, something went wrong
    raise RantParserException("[LookupBuilder::build] Error parsing dictionary lookup, probably an invalid character")
