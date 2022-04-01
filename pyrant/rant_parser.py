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
            case RantTokenType.LEFT_CURLY_BRACKET:
                tokens.pop(0)
                parser_result.append(consume_choice(tokens))
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
        tokens.pop(0)
        match token.type:
            case RantTokenType.RIGHT_ANGLE_BRACKET:
                return RantLookupObject(dictionary, form, category, label)
            case RantTokenType.PLAIN_TEXT:
                dictionary = token.value
                continue
            case RantTokenType.DOT:
                # TODO: just assuming correct formatting for now
                # come back and do real validation and error-handling
                form = tokens[0].value
                tokens.pop(0)
                continue
            case RantTokenType.HYPHEN:
                # TODO: as above
                category = tokens[0].value
                tokens.pop(0)
                continue
            case _:
                continue
                # TODO: here too
    # something went wrong, fall over
    assert False


def consume_choice(tokens: list[RantToken]) -> RantChoiceObject:
    choices = list()
    this_choice = list()
    while len(tokens) > 0:
        token = tokens[0]
        tokens.pop(0)
        match token.type:
            case RantTokenType.PIPE:
                choices.append(parse(this_choice))
                continue
            case RantTokenType.RIGHT_CURLY_BRACKET:
                choices.append(parse(this_choice))
                return RantChoiceObject(choices)
            case _:
                this_choice.append(token)
                continue
    # something went wrong, fall over
    assert False

