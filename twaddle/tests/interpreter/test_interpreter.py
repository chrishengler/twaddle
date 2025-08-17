import pytest

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
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


def test_article_in_separator():
    result = get_interpreter_output(r"[rep:2][sep: \a ]{egg}")
    assert result == "egg an egg"


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


def test_hidden():
    result = get_interpreter_output("[hide]{a secret}message")
    assert result == "message"


def test_indefinite_article_in_regex():
    result = get_interpreter_output("[//[aeiou]//:i'm \\a cat;x]")
    assert result == "x'm x cxt"
    result = get_interpreter_output("[//[aeiou]//:i'm \\a elephant;x]")
    assert result == "x'm xn xlxphxnt"


def test_gap_between_hide_function_and_block():
    result = get_interpreter_output("[hide]something {and something else}")
    assert result == "something "


def test_gap_between_rep_function_and_block():
    result = get_interpreter_output("[rep:2]something {repeating }")
    assert result == "something repeating repeating "


def test_separator_without_repetitions():
    result = get_interpreter_output("[sep:x]{hey}")
    assert result == "hey"


def test_synchronizer_persistence():
    sync_interpreter = Interpreter(LookupManager(), persistent_synchronizers=True)

    sync_sentence = "[sync:test;locked]{a|b|c}"
    first_sync = sync_interpreter.interpret_external(sync_sentence)
    second_sync = sync_interpreter.interpret_external(sync_sentence)
    assert first_sync == second_sync


def test_clear_synchronizer_persistence():
    sync_interpreter = Interpreter(LookupManager(), persistent_synchronizers=True)
    results = [sync_interpreter.interpret_external("[sync:test;locked]{a|b|c}")]
    for _ in range(0, 10):
        sync_interpreter.force_clear()
        results.append(sync_interpreter.interpret_external("[sync:test;locked]{a|b|c}"))
    assert len(set(results)) > 1


def test_clear_function_in_sentence():
    sync_interpreter = Interpreter(LookupManager(), persistent_synchronizers=True)

    sentence = "[sync:test;locked]{a|b}[clear][sync:test;locked]{a|b}"
    results = [sync_interpreter.interpret_external(sentence)]
    for _ in range(0, 15):
        results.append(sync_interpreter.interpret_external(sentence))
    assert len(set(results)) > 2


def test_clear_synchronizers_with_persistence():
    sync_interpreter = Interpreter(LookupManager(), persistent_synchronizers=True)

    sentence = "[clear][sync:test;locked]{a|b} [sync:test]{a|b}"
    results = [sync_interpreter.interpret_external(sentence)]
    for _ in range(0, 15):
        results.append(sync_interpreter.interpret_external(sentence))
    assert len(set(results)) > 1


if __name__ == "__main__":
    test_case()
