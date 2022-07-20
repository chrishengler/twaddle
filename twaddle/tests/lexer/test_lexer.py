import twaddle.lexer.lexer as lexer
from twaddle.lexer.lexer_tokens import Token, TokenType


def test_angle_brackets():
    test_string = "<>"
    result = lexer.lex(test_string)

    expected_result = [
        Token(TokenType.LEFT_ANGLE_BRACKET),
        Token(TokenType.RIGHT_ANGLE_BRACKET),
    ]

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_square_brackets():
    test_string = "[]"
    result = lexer.lex(test_string)

    expected_result = [
        Token(TokenType.LEFT_SQUARE_BRACKET),
        Token(TokenType.RIGHT_SQUARE_BRACKET),
    ]

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_curly_brackets():
    test_string = "{}"
    result = lexer.lex(test_string)

    expected_result = [
        Token(TokenType.LEFT_CURLY_BRACKET),
        Token(TokenType.RIGHT_CURLY_BRACKET),
    ]

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_pipe():
    test_string = "|"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.PIPE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_hyphen():
    test_string = "-"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.HYPHEN)

    assert len(result) == 1
    assert result[0] == expected_result


def test_semicolon():
    test_string = ";"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.SEMICOLON)

    assert len(result) == 1
    assert result[0] == expected_result


def test_colon():
    test_string = ":"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.COLON)

    assert len(result) == 1
    assert result[0] == expected_result


def test_double_colon():
    test_string = "::"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.DOUBLE_COLON)

    assert len(result) == 1
    assert result[0] == expected_result


def test_quote():
    test_string = '"'
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.QUOTE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_new_line():
    test_string = r"\n"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.NEW_LINE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_indefinite_article():
    test_string = r"\a"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.LOWER_INDEFINITE_ARTICLE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_slash():
    test_string = r"\\"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.BACKSLASH)

    assert len(result) == 1
    assert result[0] == expected_result


def test_digit():
    test_string = r"\d"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.DIGIT)

    assert len(result) == 1
    assert result[0] == expected_result


def test_plaintext():
    test_string = "hello"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.PLAIN_TEXT, "hello")

    assert len(result) == 1
    assert result[0] == expected_result


def test_exclamation_mark():
    test_string = "!"
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.EXCLAMATION_MARK)

    assert len(result) == 1
    assert result[0] == expected_result


def test_equals():
    test_string = "="
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.EQUALS)

    assert len(result) == 1
    assert result[0] == expected_result


def test_dot():
    test_string = "."
    result = lexer.lex(test_string)

    expected_result = Token(TokenType.DOT)

    assert len(result) == 1
    assert result[0] == expected_result


def test_long_string():
    test_string = (
        "angle brackets <:> curly brackets{ ::  } square brackets []plaintext-hello|"
    )
    result = lexer.lex(test_string)

    expected_result = [
        Token(TokenType.PLAIN_TEXT, "angle brackets "),
        Token(TokenType.LEFT_ANGLE_BRACKET),
        Token(TokenType.COLON),
        Token(TokenType.RIGHT_ANGLE_BRACKET),
        Token(TokenType.PLAIN_TEXT, " curly brackets"),
        Token(TokenType.LEFT_CURLY_BRACKET),
        Token(TokenType.PLAIN_TEXT, " "),
        Token(TokenType.DOUBLE_COLON),
        Token(TokenType.PLAIN_TEXT, "  "),
        Token(TokenType.RIGHT_CURLY_BRACKET),
        Token(TokenType.PLAIN_TEXT, " square brackets "),
        Token(TokenType.LEFT_SQUARE_BRACKET),
        Token(TokenType.RIGHT_SQUARE_BRACKET),
        Token(TokenType.PLAIN_TEXT, "plaintext"),
        Token(TokenType.HYPHEN),
        Token(TokenType.PLAIN_TEXT, "hello"),
        Token(TokenType.PIPE),
    ]

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_realistic_sentence():
    test_string = r"I work as \a <noun-job>"
    result = lexer.lex(test_string)

    expected_result = [
        Token(TokenType.PLAIN_TEXT, "I work as "),
        Token(TokenType.LOWER_INDEFINITE_ARTICLE),
        Token(TokenType.PLAIN_TEXT, " "),
        Token(TokenType.LEFT_ANGLE_BRACKET),
        Token(TokenType.PLAIN_TEXT, "noun"),
        Token(TokenType.HYPHEN),
        Token(TokenType.PLAIN_TEXT, "job"),
        Token(TokenType.RIGHT_ANGLE_BRACKET),
    ]

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected
