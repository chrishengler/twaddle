import unittest
from pyrant.rant_token import RantToken, RantTokenType
import pyrant.rant_lexer as RantLexer

class RantLexerTest(unittest.TestCase):
    def test_brackets(self):
        test_string = "angle brackets <> curly brackets{  } square brackets []plaintext"
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

        i=0
        self.assertEqual(len(result), len(expected_result))
        for i, res in enumerate(result):
            self.assertEqual(res,expected_result[i])


if __name__ == "main":
    test = RantLexerTest
    test.test_brackets()
