import pytest

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


def test_save_block():
    result = get_interpreter_output("[save:animal]{dog|cat|rabbit}")
    assert result == ""  # Save doesn't output anything


def test_load_saved_block():
    interpreter = Interpreter(LookupManager())
    interpreter.interpret_external("[save:animal]{dog|cat|rabbit}")
    result = interpreter.interpret_external("[load:animal]")
    assert result in ["dog", "cat", "rabbit"]


def test_load_unsaved_block():
    with pytest.raises(TwaddleInterpreterException):
        get_interpreter_output("[load:nonexistent]")


def test_save_load_preserves_block_structure():
    interpreter = Interpreter(LookupManager())
    interpreter.interpret_external("[save:complex]{[rep:2]{a|b}|[case:upper]test}")

    # Running multiple times to ensure block structure is preserved
    results = set()
    for _ in range(10):
        result = interpreter.interpret_external("[load:complex]")
        results.add(result)

    assert "aa" in results or "bb" in results or "TEST" in results


def test_save_load_with_nested_blocks():
    interpreter = Interpreter(LookupManager())
    interpreter.interpret_external("[save:nested]{{a|b}|{c|d}}")

    results = set()
    for _ in range(10):
        result = interpreter.interpret_external("[load:nested]")
        results.add(result)

    assert results.issubset({"a", "b", "c", "d"})


def test_save_load_with_synchronizer():
    interpreter = Interpreter(LookupManager())
    setup = "[save:synced][sync:test;locked]{a|b|c}"
    interpreter.interpret_external(setup)

    first = interpreter.interpret_external("[load:synced]")
    second = interpreter.interpret_external("[load:synced]")
    assert first == second  # Synchronizer should still work


def test_save_load_with_labels():
    interpreter = Interpreter(LookupManager())
    setup = "[save:labeled]{a|b|c::=test}"
    interpreter.interpret_external(setup)

    result = interpreter.interpret_external("[load:labeled]")
    assert interpreter.interpret_external("{::=test}") == result


def test_save_multiple_blocks():
    interpreter = Interpreter(LookupManager())
    interpreter.interpret_external("[save:first]{one|two}")
    interpreter.interpret_external("[save:second]{three|four}")

    first = interpreter.interpret_external("[load:first]")
    second = interpreter.interpret_external("[load:second]")

    assert first in ["one", "two"]
    assert second in ["three", "four"]
