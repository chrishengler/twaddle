import interpreter.interpreter as Interpreter
from rant_exceptions import RantInterpreterException
import pytest


def get_interpreter_output(sentence):
    return Interpreter.interpret_external(sentence)


def test_plain_text():
    hello_world = "hello, world"
    result = get_interpreter_output(hello_world)
    assert result == hello_world


def test_text_with_special_characters():
    special_characters = "|-;::/:!.="
    result = get_interpreter_output(special_characters)
    assert result == special_characters


def test_choice():
    result = get_interpreter_output("{a|b}")
    assert result == 'a' or result == 'b'


def test_unknown_function_error():
    with pytest.raises(RantInterpreterException) as e_info:
        result = get_interpreter_output("[funk]")
        assert e_info.message == "[Interpreter::run] no function found named 'funk'"


def test_repeat():
    result = get_interpreter_output("[rep:3]{a}")
    assert result == 'aaa'


def test_nested_blocks():
    result = get_interpreter_output("{{a|b}|{c|d}}")
    assert result in ['a', 'b', 'c', 'd']


def test_repeat_with_separator():
    result = get_interpreter_output("[rep:3][sep:x]{a}")
    assert result == 'axaxa'


def test_repeat_with_first_and_last():
    result = get_interpreter_output("[rep:5][first:a][last:z]{x}")
    assert result == 'axxxxzx'


def test_synchronizer_locked():
    result = get_interpreter_output(
        "[x:test;locked]{a|b|c}[x:test]{a|b|c}[x:test]{a|b|c}")
    assert result in ['aaa', 'bbb', 'ccc']


def test_synchronizer_deck():
    for _ in range(0, 10):
        result = get_interpreter_output("[x:test;deck]{a|b}[x:test]{a|b}")
        assert result in ['ab', 'ba']


def test_random_number():
    for _ in range(0, 10):
        result_10 = int(get_interpreter_output("[rand:0;10]"))
        result_negative = int(get_interpreter_output("[rand:-10;-5]"))
        result_big = int(get_interpreter_output("[rand:1000;2000]"))
        assert result_10 >= 0 and result_10 <= 10
        assert result_negative >= -10 and result_negative <= -5
        assert result_big >= 1000 and result_big <= 2000


def test_case():
    result = get_interpreter_output("[case:upper]uPpEr [case:lower]loWeR")
    assert result == "UPPER lower"
    result = get_interpreter_output("[case:title]it's a title")
    assert result == "It's A Title"
    result = get_interpreter_output(
        "[case:sentence]this is a sentence. this is another SENTENCE.")
    assert result == "This is a sentence. This is another sentence."


def test_case_block_interaction():
    result = get_interpreter_output("look, a {dog[case:upper]}!")
    assert result == "look, a dog!"
    result = get_interpreter_output("{a [case:upper]A|a [case:upper]A}") 
    assert result == "a A"
    result = get_interpreter_output("the {[case:upper]A|[case:title]A} team")
    assert result == "the A team"
    result = get_interpreter_output("[case:upper]The {cow|chicken}")
    assert result in ["THE COW", "THE CHICKEN"]
    result = get_interpreter_output("[case:title]The {[case:upper]BIG[case:lower]small}")
    assert result == "The BIGsmall"


def test_digit():
    result = get_interpreter_output(r"\d\d\d")
    for d in result:
        assert int(d)


def test_new_line():
    result = get_interpreter_output(r"hello\nworld")
    assert result == """hello
world"""


if __name__ == "__main__":
    test_case()
