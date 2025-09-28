import pytest

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager

standard_interpreter = Interpreter(LookupManager())


def get_standard_interpreter_output(sentence: str) -> str:
    return standard_interpreter.interpret_external(sentence)


def test_load_saved_block():
    result = get_standard_interpreter_output("[save:word]{word} [load:word]")
    assert result == "word word"


def test_load_unsaved_block():
    with pytest.raises(TwaddleInterpreterException) as e_info:
        get_standard_interpreter_output("[load:nonexistent]")
    assert (
        e_info.value.message
        == "[Interpreter._handle_special_functions#load] Tried to load unknown pattern 'nonexistent'"
    )


def test_save_multiple_blocks():
    result = get_standard_interpreter_output(
        "[save:first]{one} [save:second]{two} [load:first] [load:second]"
    )
    assert result == "one two one two"


def test_save_load_fails_between_non_persistent_sentences():
    get_standard_interpreter_output("[save:a]{hello}")
    with pytest.raises(TwaddleInterpreterException) as e_info:
        get_standard_interpreter_output("[load:a]")
    assert (
        e_info.value.message
        == "[Interpreter._handle_special_functions#load] Tried to load unknown pattern 'a'"
    )


def test_save_load_persistence():
    interpreter = Interpreter(LookupManager(), persistent_patterns=True)
    interpreter.interpret_external("[save:a]{hello}")
    assert interpreter.interpret_external("[load:a]") == "hello"
