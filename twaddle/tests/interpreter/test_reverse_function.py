from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


def test_reverse_basic():
    result = get_interpreter_output("[reverse]{hello world}")
    assert result == "dlrow olleh"


def test_reverse_with_nested_functions():
    result = get_interpreter_output("[reverse][case:upper]{hello}")
    assert result == "OLLEH"


def test_reverse_empty_block():
    result = get_interpreter_output("[reverse]{}")
    assert result == ""


def test_reverse_with_punctuation():
    result = get_interpreter_output("[reverse]{hello, world!}")
    assert result == "!dlrow ,olleh"


def test_reverse_with_nested_blocks():
    result = get_interpreter_output("[reverse]{[rep:2][sep:\s]{hello}}")
    assert result == "olleh olleh"


def test_reverse_special_characters():
    result = get_interpreter_output("[reverse]{hello\nworld}")
    assert result == "dlrow\nolleh"


def test_reverse_unicode():
    result = get_interpreter_output("[reverse]{héllö wörld}")
    assert result == "dlröw ölléh"
