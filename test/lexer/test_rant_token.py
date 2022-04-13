from lexer.rant_token import RantToken, RantTokenType


def test_rant_token_equality():
    plaintext = RantToken(RantTokenType.PLAIN_TEXT, "plaintext")
    duplicate_plaintext = RantToken(RantTokenType.PLAIN_TEXT, "plaintext")
    different_plaintext = RantToken(
        RantTokenType.PLAIN_TEXT, "different plaintext")
    empty_plaintext = RantToken(RantTokenType.PLAIN_TEXT)
    left_angle = RantToken(RantTokenType.LEFT_ANGLE_BRACKET)
    hyphen = RantToken(RantTokenType.HYPHEN)

    assert plaintext == duplicate_plaintext
    assert plaintext != empty_plaintext
    assert plaintext != left_angle
    assert plaintext != different_plaintext
    assert left_angle != hyphen
