import twaddle.exceptions as rant_exceptions


def test_create_lexer_exception_with_message():
    x = rant_exceptions.TwaddleLexerException("Lexer fell over")
    assert x.message == "Lexer fell over"
