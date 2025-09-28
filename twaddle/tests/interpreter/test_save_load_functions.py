import pytest

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


def test_load_saved_block():
    result = get_interpreter_output("[save:word]{word} [load:word]")
    assert result == "word word"


def test_load_unsaved_block():
    with pytest.raises(TwaddleInterpreterException) as e_info:
        get_interpreter_output("[load:nonexistent]")
    assert (
        e_info.value.message
        == "[Interpreter._handle_special_functions#load] Tried to load unknown pattern 'nonexistent'"
    )


def test_save_multiple_blocks():
    interpreter = Interpreter(LookupManager())
    result = interpreter.interpret_external(
        "[save:first]{one} [save:second]{two} [load:first] [load:second]"
    )
    assert result == "one two one two"
