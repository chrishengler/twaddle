import unittest
from rant_token import RantToken, RantTokenType
import rant_lexer as RantLexer

class RantLexerTest(unittest.TestCase):
    def test_brackets(self):
        test_string = "angle brackets <> curly brackets{  } square brackets []plaintext-hello|"
        result = RantLexer.lex(test_string)

        expected_result = []
        expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, "angle brackets "))
        expected_result.append(RantToken(RantTokenType.LEFT_ANGLE_BRACKET))
        expected_result.append(RantToken(RantTokenType.RIGHT_ANGLE_BRACKET))
        expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, " curly brackets"))
        expected_result.append(RantToken(RantTokenType.LEFT_CURLY_BRACKET))
        expected_result.append(RantToken(RantTokenType.PLAIN_TEXT,"  "))
        expected_result.append(RantToken(RantTokenType.RIGHT_CURLY_BRACKET))
        expected_result.append(RantToken(RantTokenType.PLAIN_TEXT, " square brackets "))
        expected_result.append(RantToken(RantTokenType.LEFT_SQUARE_BRACKET))
        expected_result.append(RantToken(RantTokenType.RIGHT_SQUARE_BRACKET))
        expected_result.append(RantToken(RantTokenType.PLAIN_TEXT,"plaintext"))
        expected_result.append(RantToken(RantTokenType.HYPHEN))
        expected_result.append(RantToken(RantTokenType.PLAIN_TEXT,"hello"))
        expected_result.append(RantToken(RantTokenType.PIPE))

        i=0
        assert(len(result) == len(expected_result))
        for i, res in enumerate(result):
            assert(res == expected_result[i])


if __name__ == "main":
    test = RantLexerTest
    test.test_brackets()
