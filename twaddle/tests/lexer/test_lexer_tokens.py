from twaddle.lexer.lexer_tokens import Token, TokenType


def test_rant_token_equality():
    plaintext = Token(TokenType.PLAIN_TEXT, "plaintext")
    duplicate_plaintext = Token(TokenType.PLAIN_TEXT, "plaintext")
    different_plaintext = Token(TokenType.PLAIN_TEXT, "different plaintext")
    empty_plaintext = Token(TokenType.PLAIN_TEXT)
    left_angle = Token(TokenType.LEFT_ANGLE_BRACKET)
    hyphen = Token(TokenType.HYPHEN)

    assert plaintext == duplicate_plaintext
    assert plaintext != empty_plaintext
    assert plaintext != left_angle
    assert plaintext != different_plaintext
    assert left_angle != hyphen
