import unittest
from rant_token import RantToken, RantTokenType
import rant_lexer as RantLexer


def test_angle_brackets():
    test_string = "<>"
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(RantToken(RantTokenType.LEFT_ANGLE_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_ANGLE_BRACKET))

    assert(len(result) == len(expected_result))
    for actual, expected in zip(result, expected_result):
        assert(actual == expected)


def test_square_brackets():
    test_string = "[]"
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(RantToken(RantTokenType.LEFT_SQUARE_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_SQUARE_BRACKET))

    assert(len(result) == len(expected_result))
    for actual, expected in zip(result, expected_result):
        assert(actual == expected)


def test_curly_brackets():
    test_string = "{}"
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(RantToken(RantTokenType.LEFT_CURLY_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_CURLY_BRACKET))

    assert(len(result) == len(expected_result))
    for actual, expected in zip(result, expected_result):
        assert(actual == expected)


def test_pipe():
    test_string = "|"
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.PIPE)

    assert(len(result) == 1)
    assert(result[0] == expected_result)


def test_hyphen():
    test_string = "-"
    result = RantLexer.lex(test_string)

    expected_result = RantToken(RantTokenType.HYPHEN)

    assert(len(result) == 1)
    assert(result[0] == expected_result)


def test_long_string():
    test_string = "angle brackets <> curly brackets{  } square brackets []plaintext-hello|"
    result = RantLexer.lex(test_string)

    expected_result = []
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, "angle brackets "))
    expected_result.append(RantToken(RantTokenType.LEFT_ANGLE_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_ANGLE_BRACKET))
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, " curly brackets"))
    expected_result.append(RantToken(RantTokenType.LEFT_CURLY_BRACKET))
    expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, "  "))
    expected_result.append(RantToken(RantTokenType.RIGHT_CURLY_BRACKET))
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, " square brackets "))
    expected_result.append(RantToken(RantTokenType.LEFT_SQUARE_BRACKET))
    expected_result.append(RantToken(RantTokenType.RIGHT_SQUARE_BRACKET))
    expected_result.append(
        RantToken(RantTokenType.PLAIN_TEXT, "plaintext"))
    expected_result.append(RantToken(RantTokenType.HYPHEN))
    expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, "hello"))
    expected_result.append(RantToken(RantTokenType.PIPE))

    i = 0
    assert(len(result) == len(expected_result))
    for actual, expected in zip(result, expected_result):
        assert(actual == expected)
