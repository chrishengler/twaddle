import pytest

import twaddle.interpreter.interpreter as interpreter
from twaddle.exceptions import TwaddleInterpreterException


def get_interpreter_output(sentence):
    return interpreter.interpret_external(sentence)


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
    assert result == "a" or result == "b"


def test_unknown_function_error():
    with pytest.raises(TwaddleInterpreterException) as e_info:
        get_interpreter_output("[funk]")
        assert e_info.message == "[Interpreter::run] no function found named 'funk'"


def test_repeat():
    result = get_interpreter_output("[rep:3]{a}")
    assert result == "aaa"


def test_nested_blocks():
    result = get_interpreter_output("{{a|b}|{c|d}}")
    assert result in ["a", "b", "c", "d"]


# noinspection SpellCheckingInspection
def test_repeat_with_separator():
    result = get_interpreter_output("[rep:3][sep:x]{a}")
    assert result == "axaxa"


# noinspection SpellCheckingInspection
def test_repeat_with_first_and_last():
    result = get_interpreter_output("[rep:5][first:a][last:z]{x}")
    assert result == "axxxxzx"


def test_synchronizer_locked():
    result = get_interpreter_output(
        "[x:tests;locked]{a|b|c}[x:tests]{a|b|c}[x:tests]{a|b|c}"
    )
    assert result in ["aaa", "bbb", "ccc"]


def test_synchronizer_deck():
    for _ in range(0, 10):
        result = get_interpreter_output("[x:tests;deck]{a|b}[x:tests]{a|b}")
        assert result in ["ab", "ba"]


def test_random_number():
    for _ in range(0, 10):
        result_10 = int(get_interpreter_output("[rand:0;10]"))
        result_negative = int(get_interpreter_output("[rand:-10;-5]"))
        result_big = int(get_interpreter_output("[rand:1000;2000]"))
        assert 0 <= result_10 <= 10
        assert -10 <= result_negative <= -5
        assert 1000 <= result_big <= 2000


def test_case():
    # result = get_interpreter_output("[case:upper]uPpEr [case:lower]loWeR")
    # assert result == "UPPER lower"
    # result = get_interpreter_output("[case:title]it's a title")
    # assert result == "It's A Title"
    result = get_interpreter_output("\\a [case:title]egg")
    assert result == "an Egg"
    result = get_interpreter_output(
        "[case:sentence]this is a sentence. this is another SENTENCE."
    )
    assert result == "This is a sentence. This is another sentence."


# noinspection SpellCheckingInspection
def test_case_block_interaction():
    result = get_interpreter_output("look, a {dog[case:upper]}!")
    assert result == "look, a dog!"
    result = get_interpreter_output("{a [case:upper]A|a [case:upper]A}")
    assert result == "a A"
    result = get_interpreter_output("the {[case:title]A} team")
    assert result == "the A Team"
    result = get_interpreter_output("[case:upper]The {cow|chicken}")
    assert result in ["THE COW", "THE CHICKEN"]
    result = get_interpreter_output(
        "[case:title]The {[case:upper]BIG[case:lower]small}"
    )
    assert result == "The BIGsmall"


def test_digit():
    result = get_interpreter_output(r"\d\d\d")
    for d in result:
        int(d)


# noinspection SpellCheckingInspection
def test_new_line():
    result = get_interpreter_output(r"hello\nworld!")
    assert (
        result
        == """hello
world!"""
    )


def test_simple_regex():
    result = get_interpreter_output("[//a//i:a bat;i]")
    assert result == "i bit"
    result = get_interpreter_output("[//a//i:a;[match][match]]")
    assert result == "aa"


def test_indefinite_article_in_regex():
    result = get_interpreter_output("[//[aeiou]//:i'm \\a cat;x]")
    assert result == "x'm x cxt"
    result = get_interpreter_output("[//[aeiou]//:i'm \\a elephant;x]")
    assert result == "x'm xn xlxphxnt"


if __name__ == "__main__":
    test_case()
