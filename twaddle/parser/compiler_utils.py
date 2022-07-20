from collections import deque

from twaddle.exceptions import TwaddleParserException
from twaddle.lexer.lexer_tokens import Token, TokenType
from twaddle.parser.compiler_objects import TextObject


def to_plain_text_token(raw: Token) -> Token:
    match raw.type:
        case TokenType.PLAIN_TEXT:
            return raw
        case TokenType.EXCLAMATION_MARK:
            return Token(TokenType.PLAIN_TEXT, "!")
        case TokenType.COLON:
            return Token(TokenType.PLAIN_TEXT, ":")
        case TokenType.SEMICOLON:
            return Token(TokenType.PLAIN_TEXT, ";")
        case TokenType.PIPE:
            return Token(TokenType.PLAIN_TEXT, "|")
        case TokenType.HYPHEN:
            return Token(TokenType.PLAIN_TEXT, "-")
        case TokenType.DOUBLE_COLON:
            return Token(TokenType.PLAIN_TEXT, "::")
        case TokenType.BACKSLASH:
            return Token(TokenType.PLAIN_TEXT, "/")
        case TokenType.DOT:
            return Token(TokenType.PLAIN_TEXT, ".")
        case TokenType.EQUALS:
            return Token(TokenType.PLAIN_TEXT, "=")
        # unrecognised token type
        # should throw an error here once everything's ready
        case _:
            return Token(TokenType.PLAIN_TEXT, raw.value)


def to_plain_text_object(raw: Token) -> TextObject:
    return TextObject(get_text_for_object(raw))


def get_text_for_object(raw: Token) -> str:
    match raw.type:
        case TokenType.LEFT_ANGLE_BRACKET:
            return "<"
        case TokenType.RIGHT_ANGLE_BRACKET:
            return ">"
        case TokenType.LEFT_CURLY_BRACKET:
            return "{"
        case TokenType.RIGHT_CURLY_BRACKET:
            return "}"
        case TokenType.LEFT_SQUARE_BRACKET:
            return "["
        case TokenType.RIGHT_SQUARE_BRACKET:
            return "]"
        case TokenType.PIPE:
            return "|"
        case TokenType.HYPHEN:
            return "-"
        case TokenType.SEMICOLON:
            return ";"
        case TokenType.COLON:
            return ":"
        case TokenType.DOUBLE_COLON:
            return "::"
        case TokenType.QUOTE:
            return '"'
        case TokenType.NEW_LINE:
            return "\n"
        case TokenType.TAB:
            return "\t"
        case TokenType.LOWER_INDEFINITE_ARTICLE:
            return r"\a"
        case TokenType.UPPER_INDEFINITE_ARTICLE:
            return r"\A"
        case TokenType.BACKSLASH:
            return "\\"
        case TokenType.FORWARD_SLASH:
            return "/"
        case TokenType.REGEX:
            return "//"
        case TokenType.DIGIT:
            return r"\d"
        case TokenType.EXCLAMATION_MARK:
            return "!"
        case TokenType.DOT:
            return "."
        case TokenType.EQUALS:
            return "="
        case TokenType.PLAIN_TEXT:
            return raw.value
        # unrecognised token type
        case _:
            raise TwaddleParserException(
                f"[get_plain_text_for_object] unknown token type: {raw.type}"
            )


def to_plain_text_token_except(raw: Token, accept_list: tuple[TokenType]) -> Token:
    if raw.type in accept_list:
        return raw
    else:
        return to_plain_text_token(raw)


def merge_text_objects(raw: deque[TextObject]) -> TextObject:
    value = ""

    for token in raw:
        if isinstance(token, TextObject):
            value += token.text
        else:
            raise TwaddleParserException(
                f"[ParserUtils::merge_text_objects] object of type {type(token)} when RantTextObject was expected"
            )
    return TextObject(value)
