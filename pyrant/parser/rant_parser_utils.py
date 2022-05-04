from collections import deque
from parser.rant_object import *
from lexer.rant_token import *
from rant_exceptions import RantParserException


def to_plain_text_token(raw: RantToken) -> RantToken:
    match raw.type:
        case RantTokenType.PLAIN_TEXT:
            return raw
        case RantTokenType.EXCLAMATION_MARK:
            return RantToken(RantTokenType.PLAIN_TEXT, '!')
        case RantTokenType.COLON:
            return RantToken(RantTokenType.PLAIN_TEXT, ':')
        case RantTokenType.SEMICOLON:
            return RantToken(RantTokenType.PLAIN_TEXT, ';')
        case RantTokenType.PIPE:
            return RantToken(RantTokenType.PLAIN_TEXT, '|')
        case RantTokenType.HYPHEN:
            return RantToken(RantTokenType.PLAIN_TEXT, '-')
        case RantTokenType.DOUBLE_COLON:
            return RantToken(RantTokenType.PLAIN_TEXT, '::')
        case RantTokenType.SLASH:
            return RantToken(RantTokenType.PLAIN_TEXT, '/')
        case RantTokenType.DOT:
            return RantToken(RantTokenType.PLAIN_TEXT, '.')
        case RantTokenType.EQUALS:
            return RantToken(RantTokenType.PLAIN_TEXT, '=')

        # unrecognised token type
        # should throw an error here once everything's ready
        case _:
            return RantToken(RantTokenType.PLAIN_TEXT, raw.value)


def to_plain_text_object(raw: RantToken) -> RantTextObject:
    match raw.type:
        case RantTokenType.PLAIN_TEXT:
            return RantTextObject(raw.value)
        case RantTokenType.EXCLAMATION_MARK:
            return RantTextObject('!')
        case RantTokenType.COLON:
            return RantTextObject(':')
        case RantTokenType.SEMICOLON:
            return RantTextObject(';')
        case RantTokenType.PIPE:
            return RantTextObject('|')
        case RantTokenType.HYPHEN:
            return RantTextObject('-')
        case RantTokenType.DOUBLE_COLON:
            return RantTextObject('::')
        case RantTokenType.SLASH:
            return RantTextObject('/')
        case RantTokenType.DOT:
            return RantTextObject('.')
        case RantTokenType.EQUALS:
            return RantTextObject('=')

        # unrecognised token type
        # should throw an error here once everything's ready
        case _:
            pass


def to_plain_text_token_except(raw: RantToken, accept_list: tuple[RantTokenType]) -> RantToken:
    if raw.type in accept_list:
        return raw
    else:
        return to_plain_text_token


def to_plain_text_object_except(raw: RantToken, accept_list: tuple[RantTokenType]) -> RantObject:
    if raw.type in accept_list:
        return raw
    else:
        return to_plain_text_object


def merge_text_objects(raw: deque[RantTextObject]) -> RantTextObject:
    value = ''

    for token in raw:
        if isinstance(token, RantTextObject):
            value += token.text
        else:
            raise RantParserException(f"[ParserUtils::merge_text_objects] object of type {typeof(token)} when RantTextObject was expected")
    return RantTextObject(value)
