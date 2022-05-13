from interpreter.formatting_strategy import FormattingStrategy
import interpreter.formatter as Formatter


def test_simple_print():
    Formatter.append("hello")
    assert Formatter.get() == "hello"

def test_normal_upper():
    Formatter.append("abc")
    Formatter.set_strategy(FormattingStrategy.UPPER)
    Formatter.append("def")
    assert Formatter.get() == "abcDEF"

def test_upper_lower():
    Formatter.append("abc")
    Formatter.set_strategy(FormattingStrategy.UPPER)
    Formatter.append("def")
    Formatter.set_strategy(FormattingStrategy.LOWER)
    Formatter.append("GHI")
    assert Formatter.get() == "abcDEFghi"

def test_sentence():
    Formatter.set_strategy(FormattingStrategy.SENTENCE)
    Formatter.append("hey there! this is. a test")
    assert Formatter.get() == "Hey there! This is. A test"

def test_title():
    Formatter.set_strategy(FormattingStrategy.TITLE)
    Formatter.append("hey there! this text's a test")
    assert Formatter.get() == "Hey There! This Text's A Test"

if __name__ == "__main__":
    test_sentence()
