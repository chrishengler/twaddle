from types import WrapperDescriptorType
from rant_object import *


def parse(tokens: list[RantToken]) -> list[RantObject]:
    parser_result = list()
    i = 0

    while len(tokens) > 0:
        token = tokens[0]
        match token.type:
            case RantTokenType.PLAIN_TEXT:
                parser_result.append(RantTextObject(token.value))
                tokens.pop(0)
                continue
            case RantTokenType.LEFT_ANGLE_BRACKET:
                tokens.pop(0)
                parser_result.append(consume_lookup(tokens))
                continue
            case _:
                # should throw an error here once everything's ready
                tokens.pop(0)
    return parser_result


def consume_lookup(tokens: list[RantToken]) -> RantLookupObject:
    dictionary = ""
    form = ""
    category = ""
    label = ""
    while len(tokens) > 0:
        token = tokens[0]
        match token.type:
            case RantTokenType.RIGHT_ANGLE_BRACKET:
                tokens.pop(0)
                return RantLookupObject(dictionary, form, category, label)
            case RantTokenType.PLAIN_TEXT:
                dictionary = token.value
                tokens.pop(0)
                continue
            case RantTokenType.DOT:
                # TODO: just assuming correct formatting for now
                # come back and do real validation and error-handling
                tokens.pop(0)
                form = tokens[0].value
                tokens.pop(0)
                continue
            case RantTokenType.HYPHEN:
                # TODO: as above
                tokens.pop(0)
                category = tokens[0].value
                tokens.pop(0)
                continue
            case _:
                # TODO: here too
                tokens.pop(0)
    # something went wrong, fall over
    assert False




