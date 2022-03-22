import pytest

from rant_token import RantToken, RantTokenType
from rant_exceptions import RantLexerException
import rant_lexer as RantLexer


def test_angle_brackets():
    test_string = '<>'
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(RantToken(RantTokenType.LEFT_ANGLE_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_ANGLE_BRACKET))

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_square_brackets():
    test_string = '[]'
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(RantToken(RantTokenType.LEFT_SQUARE_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_SQUARE_BRACKET))

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_curly_brackets():
    test_string = '{}'
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(RantToken(RantTokenType.LEFT_CURLY_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_CURLY_BRACKET))

    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_pipe():
    test_string = '|'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.PIPE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_hyphen():
    test_string = '-'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.HYPHEN)

    assert len(result) == 1
    assert result[0] == expected_result


def test_colon():
    test_string = ':'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.COLON)

    assert len(result)==1
    assert result[0] == expected_result

def test_double_colon():
    test_string = '::'
    result = RantLexer.lex(test_string)
    
    expected_result = RantToken(RantTokenType.DOUBLE_COLON)
    
    assert len(result) == 1
    assert result[0] == expected_result

def test_quote():
    test_string = '"'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.QUOTE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_new_line():
    test_string = r'\n'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.NEW_LINE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_indefinite_article():
    test_string = r'\a'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.INDEFINITE_ARTICLE)

    assert len(result) == 1
    assert result[0] == expected_result


def test_slash():
    test_string = r'\\'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.SLASH)

    assert len(result) == 1
    assert result[0] == expected_result


def test_digit():
    test_string = r'\d'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.DIGIT)

    assert len(result) == 1
    assert result[0] == expected_result

    
def test_plaintext():
    test_string = 'hello'
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.PLAIN_TEXT, 'hello')

    assert len(result) == 1
    assert result[0] == expected_result


def test_long_string():
    test_string = 'angle brackets <:> curly brackets{ ::  } square brackets []plaintext-hello|'
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, 'angle brackets '))
    expected_result.append(RantToken(RantTokenType.LEFT_ANGLE_BRACKET))
    expected_result.append(RantToken(RantTokenType.COLON))
    expected_result.append(RantToken(RantTokenType.RIGHT_ANGLE_BRACKET))
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, ' curly brackets'))
    expected_result.append(RantToken(RantTokenType.LEFT_CURLY_BRACKET))
    expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, ' '))
    expected_result.append(RantToken(RantTokenType.DOUBLE_COLON))
    expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, '  '))
    expected_result.append(RantToken(RantTokenType.RIGHT_CURLY_BRACKET))
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, ' square brackets '))
    expected_result.append(RantToken(RantTokenType.LEFT_SQUARE_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_SQUARE_BRACKET))
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, 'plaintext'))
    expected_result.append(RantToken(RantTokenType.HYPHEN))
    expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, 'hello'))
    expected_result.append(RantToken(RantTokenType.PIPE))

    i = 0
    assert len(result) == len(expected_result)
    for actual, expected in zip(result, expected_result):
        assert actual == expected


def test_throws_on_invalid_escape():
    test_string = r'\m'
    with pytest.raises(RantLexerException) as rle:
        result = RantLexer.lex(test_string)
    assert rle.value.message == f"Unknown escape code '\\m'"

def test_throws_when_escaping_nothing():
    test_string = '\\'
    with pytest.raises(RantLexerException) as rle:
        result = RantLexer.lex(test_string)
    assert rle.value.message == f"Tried to escape nothing"
