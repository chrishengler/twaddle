from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


def test_while_counting_up():
    sentence = (
        "[copy:var]{1 }[while:[lt:[paste:var];5]]{[copy:var]{[add:[paste:var];1]} }"
    )
    assert get_interpreter_output(sentence) == "1 2 3 4 5 "


def test_while_iteration_limit():
    sentence = "[while:[bool:1];5]{[rand:0;9]}"
    assert len(get_interpreter_output(sentence)) == 5
