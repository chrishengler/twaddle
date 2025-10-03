import pytest

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager

standard_interpreter = Interpreter(LookupManager())


def get_standard_interpreter_output(sentence: str) -> str:
    return standard_interpreter.interpret_external(sentence)


def test_paste_copyd_block():
    result = get_standard_interpreter_output("[copy:word]{word} [paste:word]")
    assert result == "word word"


def test_paste_uncopyd_block():
    with pytest.raises(TwaddleInterpreterException) as e_info:
        get_standard_interpreter_output("[paste:nonexistent]")
    assert (
        e_info.value.message
        == "[Interpreter._handle_special_functions#paste] Tried to paste result of unknown block 'nonexistent'"
    )


def test_copy_multiple_blocks():
    result = get_standard_interpreter_output(
        "[copy:first]{one} [copy:second]{two} [paste:first] [paste:second]"
    )
    assert result == "one two one two"


def test_copy_paste_fails_between_non_persistent_sentences():
    get_standard_interpreter_output("[copy:a]{hello}")
    with pytest.raises(TwaddleInterpreterException) as e_info:
        get_standard_interpreter_output("[paste:a]")
    assert (
        e_info.value.message
        == "[Interpreter._handle_special_functions#paste] Tried to paste result of unknown block 'a'"
    )


def test_copy_paste_persistence():
    interpreter = Interpreter(LookupManager(), persistent_clipboard=True)
    interpreter.interpret_external("[copy:a]{hello}")
    assert interpreter.interpret_external("[paste:a]") == "hello"
