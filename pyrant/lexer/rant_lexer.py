from collections import deque
from rant_exceptions import RantLexerException
from lexer.rant_token import RantToken, RantTokenType


def lex(input_str: str) -> deque[RantToken]:
    output = deque()

    i = 0
    while i < len(input_str):
        next_token, length = _get_token_type(input_str[i:])
        if next_token is not RantTokenType.PLAIN_TEXT:
            output.append(RantToken(next_token))
            i += length
        else:
            text, length = _consume_plain_text(input_str[i:])
            output.append(text)
            i += length

    return output


def _get_token_type(input_str: str) -> tuple[RantToken, int]:
    assert(len(input_str) != 0)
    match input_str[0]:
        case '<': return RantTokenType.LEFT_ANGLE_BRACKET, 1
        case '>': return RantTokenType.RIGHT_ANGLE_BRACKET, 1
        case '{': return RantTokenType.LEFT_CURLY_BRACKET, 1
        case '}': return RantTokenType.RIGHT_CURLY_BRACKET, 1
        case '[': return RantTokenType.LEFT_SQUARE_BRACKET, 1
        case ']': return RantTokenType.RIGHT_SQUARE_BRACKET, 1
        case '|': return RantTokenType.PIPE, 1
        case '-': return RantTokenType.HYPHEN, 1
        case ':':
            if len(input_str) > 1 and input_str[1] == ':':
                return RantTokenType.DOUBLE_COLON, 2
            else:
                return RantTokenType.COLON, 1
        case ';': return RantTokenType.SEMICOLON, 1
        case '\\':
            if len(input_str) > 1:
                if input_str[1] == 'n':
                    return RantTokenType.NEW_LINE, 2
                elif input_str[1] == 'a':
                    return RantTokenType.LOWER_INDEFINITE_ARTICLE, 2
                elif input_str[1] == 'A':
                    return RantTokenType.UPPER_INDEFINITE_ARTICLE, 2
                elif input_str[1] == '\\':
                    return RantTokenType.SLASH, 2
                elif input_str[1] == 'd':
                    return RantTokenType.DIGIT, 2
                elif input_str[1] == 't':
                    return RantTokenType.TAB, 2
                raise RantLexerException(
                    f"Unknown escape code '\\{input_str[1]}'")
            else:
                raise RantLexerException(f"Tried to escape nothing")
        case '"': return RantTokenType.QUOTE, 1
        case '!': return RantTokenType.EXCLAMATION_MARK, 1
        case '=': return RantTokenType.EQUALS, 1
        case '.': return RantTokenType.DOT, 1
        case _: return RantTokenType.PLAIN_TEXT, 0


def _consume_plain_text(input_str: str) -> tuple[str, int]:
    i = 0
    while i < len(input_str):
        next_type, _ = _get_token_type(input_str[i:])
        if next_type is not RantTokenType.PLAIN_TEXT:
            return RantToken(RantTokenType.PLAIN_TEXT, input_str[:i]), i
        else:
            i += 1

    return RantToken(RantTokenType.PLAIN_TEXT, input_str), len(input_str)
