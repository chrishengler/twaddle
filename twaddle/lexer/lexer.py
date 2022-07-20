from collections import deque

from twaddle.lexer.lexer_tokens import Token, TokenType


def lex(input_str: str) -> deque[Token]:
    output = deque()

    i = 0
    while i < len(input_str):
        next_token, length = _get_token_type(input_str[i:])
        if next_token is not TokenType.PLAIN_TEXT:
            output.append(Token(next_token))
            i += length
        else:
            text, length = _consume_plain_text(input_str[i:])
            output.append(text)
            i += length

    return output


def _get_token_type(input_str: str) -> tuple[TokenType, int]:
    assert len(input_str) != 0
    match input_str[0]:
        case "<":
            return TokenType.LEFT_ANGLE_BRACKET, 1
        case ">":
            return TokenType.RIGHT_ANGLE_BRACKET, 1
        case "{":
            return TokenType.LEFT_CURLY_BRACKET, 1
        case "}":
            return TokenType.RIGHT_CURLY_BRACKET, 1
        case "[":
            return TokenType.LEFT_SQUARE_BRACKET, 1
        case "]":
            return TokenType.RIGHT_SQUARE_BRACKET, 1
        case "|":
            return TokenType.PIPE, 1
        case "-":
            return TokenType.HYPHEN, 1
        case ":":
            if len(input_str) > 1 and input_str[1] == ":":
                return TokenType.DOUBLE_COLON, 2
            else:
                return TokenType.COLON, 1
        case ";":
            return TokenType.SEMICOLON, 1
        case "\\":
            if len(input_str) > 1:
                match input_str[1]:
                    case "n":
                        return TokenType.NEW_LINE, 2
                    case "a":
                        return TokenType.LOWER_INDEFINITE_ARTICLE, 2
                    case "A":
                        return TokenType.UPPER_INDEFINITE_ARTICLE, 2
                    case "\\":
                        return TokenType.BACKSLASH, 2
                    case "d":
                        return TokenType.DIGIT, 2
                    case "t":
                        return TokenType.TAB, 2
                    case _:
                        """
                        this isn't ideal but avoids having to define special
                        tokens which only have meaning in regices
                        """
                        return TokenType.BACKSLASH, 1
        case '"':
            return TokenType.QUOTE, 1
        case "!":
            return TokenType.EXCLAMATION_MARK, 1
        case "=":
            return TokenType.EQUALS, 1
        case ".":
            return TokenType.DOT, 1
        case "/":
            if len(input_str) > 1 and input_str[1] == "/":
                return TokenType.REGEX, 2
            else:
                return TokenType.FORWARD_SLASH, 1
        case _:
            return TokenType.PLAIN_TEXT, 0


def _consume_plain_text(input_str: str) -> tuple[Token, int]:
    i = 0
    while i < len(input_str):
        next_type, _ = _get_token_type(input_str[i:])
        if next_type is not TokenType.PLAIN_TEXT:
            return Token(TokenType.PLAIN_TEXT, input_str[:i]), i
        else:
            i += 1

    return Token(TokenType.PLAIN_TEXT, input_str), len(input_str)
