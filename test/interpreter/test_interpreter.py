import interpreter.interpreter as Interpreter
import parser.rant_parser as Parser
import lexer.rant_lexer as Lexer
from rant_exceptions import RantInterpreterException
import pytest


def get_interpreter_output(sentence):
    return Interpreter.interpret_internal(Parser.parse(Lexer.lex(sentence)))


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


def test_repeat_with_separator():
    result = get_interpreter_output("[rep:3][sep:x]{a}")
    assert result == 'axaxa'


def test_repeat_with_first_and_last():
    result = get_interpreter_output("[rep:5][first:a][last:z]{x}")
    assert result == 'axxxxzx'


def test_random_number():
    for _ in range(0,10):
        result_10 = int(get_interpreter_output("[rand:0;10]"))
        result_negative = int(get_interpreter_output("[rand:-10;-5]"))
        result_big = int(get_interpreter_output("[rand:1000;2000]"))
        assert result_10 >= 0 and result_10 <= 10
        assert result_negative >= -10 and result_negative <= -5
        assert result_big >= 1000 and result_big <= 2000


if __name__ == "__main__":
    test_random_number()
