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
    return RantTextObject(get_plain_text_for_object(raw))


def get_plain_text_for_object(raw: RantToken) -> str:
    match raw.type:
        case RantTokenType.LEFT_ANGLE_BRACKET:
            return '<'
        case RantTokenType.RIGHT_ANGLE_BRACKET:
            return '>'
        case RantTokenType.LEFT_CURLY_BRACKET:
            return '{'
        case RantTokenType.RIGHT_CURLY_BRACKET:
            return '}'
        case RantTokenType.LEFT_SQUARE_BRACKET:
            return '['
        case RantTokenType.RIGHT_SQUARE_BRACKET:
            return ']'
        case RantTokenType.PIPE:
            return '|'
        case RantTokenType.HYPHEN:
            return '-'
        case RantTokenType.SEMICOLON:
            return ';'
        case RantTokenType.COLON:
            return ':'
        case RantTokenType.DOUBLE_COLON:
            return '::'
        case RantTokenType.QUOTE:
            return '"'
        case RantTokenType.NEW_LINE:
            return '\n'
        case RantTokenType.LOWER_INDEFINITE_ARTICLE:
            return '\a'
        case RantTokenType.UPPER_INDEFINITE_ARTICLE:
            return '\A'
        case RantTokenType.SLASH:
            return '\'
        case RantTokenType.DIGIT:
            return '\d'
        case RantTokenType.EXCLAMATION_MARK:
            return '!'
        case RantTokenType.DOT:
            return '.'
        case RantTokenType.EQUALS:
            return '='
        case RantTokenType.PLAIN_TEXT:
            return raw.value
        # unrecognised token type
        case _:
            raise RantParserException(
                f"[get_plain_text_for_object] unknown token type: {raw.type}")


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
            raise RantParserException(
                f"[ParserUtils::merge_text_objects] object of type {typeof(token)} when RantTextObject was expected")
    return RantTextObject(value)
