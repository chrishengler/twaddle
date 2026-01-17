from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


def test_basic_while():
    sentence = (
        "[copy:var]{1 }[while:[lt:[paste:var];5]]{[copy:var]{[add:[paste:var];1]} }"
    )
    assert get_interpreter_output(sentence) == "1 2 3 4 5 "
