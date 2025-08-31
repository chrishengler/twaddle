from twaddle.interpreter.formatter import Formatter
from twaddle.interpreter.formatting_object import FormattingStrategy

formatter = Formatter()


def test_simple_print():
    formatter.append("hello")
    assert formatter.resolve() == "hello"


def test_normal_upper():
    formatter.append("abc")
    formatter.set_strategy(FormattingStrategy.UPPER)
    formatter.append("def")
    assert formatter.resolve() == "abcDEF"


# noinspection SpellCheckingInspection
def test_upper_lower():
    formatter.append("abc")
    formatter.set_strategy(FormattingStrategy.UPPER)
    formatter.append("def")
    formatter.set_strategy(FormattingStrategy.LOWER)
    formatter.append("GHI")
    assert formatter.resolve() == "abcDEFghi"


def test_sentence():
    formatter.set_strategy(FormattingStrategy.SENTENCE)
    formatter.append("hey there! this is. a test")
    assert formatter.resolve() == "Hey there! This is. A test"


def test_sentence_with_i():
    formatter.set_strategy(FormattingStrategy.SENTENCE)
    formatter.append("will this work how I expect?")
    assert formatter.resolve() == "Will this work how I expect?"


def test_i_edge_cases():
    formatter.set_strategy(FormattingStrategy.SENTENCE)
    formatter.append("ii i5 i! i i I i.")
    assert formatter.resolve() == "Ii i5 I! I I I I."


def test_title():
    formatter.set_strategy(FormattingStrategy.TITLE)
    formatter.append("hey there! this text's a test")
    assert formatter.resolve() == "Hey There! This Text's A Test"


if __name__ == "__main__":
    test_sentence()
