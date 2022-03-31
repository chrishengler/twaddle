from types import WrapperDescriptorType
from rant_object import *


def parse(tokens: list[RantToken]) -> list[RantObject]:
    parser_result = list()
    for token in tokens:
        match token.type: 
            case RantObjectType.TEXT: parser_result.append(RantTextObject(token.text))
    return parser_result

