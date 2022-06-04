from pyrant.interpreter.formatting_object import FormattingStrategy
from pyrant.interpreter.formatter import Formatter

formatter = Formatter()

def test_simple_print():
    formatter.append("hello")
    assert formatter.get() == "hello"


def test_normal_upper():
    formatter.append("abc")
    formatter.set_strategy(FormattingStrategy.UPPER)
    formatter.append("def")
    assert formatter.get() == "abcDEF"


# noinspection SpellCheckingInspection
def test_upper_lower():
    formatter.append("abc")
    formatter.set_strategy(FormattingStrategy.UPPER)
    formatter.append("def")
    formatter.set_strategy(FormattingStrategy.LOWER)
    formatter.append("GHI")
    assert formatter.get() == "abcDEFghi"


def test_sentence():
    formatter.set_strategy(FormattingStrategy.SENTENCE)
    formatter.append("hey there! this is. a test")
    assert formatter.get() == "Hey there! This is. A test"


def test_title():
    formatter.set_strategy(FormattingStrategy.TITLE)
    formatter.append("hey there! this text's a test")
    assert formatter.get() == "Hey There! This Text's A Test"


if __name__ == "__main__":
    test_sentence()
