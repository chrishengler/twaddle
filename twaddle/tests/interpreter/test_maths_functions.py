import pytest

from twaddle.exceptions import TwaddleFunctionException
from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


def test_add_simple():
    result = get_interpreter_output("[add:1;1]")
    assert result == "2"


def test_add_negative():
    result = get_interpreter_output("[add:1;-5]")
    assert result == "-4"


def test_add_zero():
    result = get_interpreter_output("[add:3;0]")
    assert result == "3"


def test_add_many():
    result = get_interpreter_output("[add:3;5;2]")
    assert result == "10"


def test_add_non_integer():
    result = get_interpreter_output("[add:4.2;5.7]")
    assert result == "9.9"


def test_subtract_simple():
    result = get_interpreter_output("[subtract:1;1]")
    assert result == "0"


def test_subtract_negative():
    result = get_interpreter_output("[subtract:1;-5]")
    assert result == "6"


def test_subtract_zero():
    result = get_interpreter_output("[subtract:3;0]")
    assert result == "3"


def test_subtract_many():
    result = get_interpreter_output("[subtract:3;5;2]")
    assert result == "-4"


def test_subtract_non_integer():
    result = get_interpreter_output("[subtract:4.2;5.7]")
    assert result == "-1.5"


def test_multiply_simple():
    result = get_interpreter_output("[multiply:2;3]")
    assert result == "6"


def test_multiply_negative():
    result = get_interpreter_output("[multiply:2;-5]")
    assert result == "-10"


def test_multiply_zero():
    result = get_interpreter_output("[multiply:3;0]")
    assert result == "0"


def test_multiply_many():
    result = get_interpreter_output("[multiply:3;5;2]")
    assert result == "30"


def test_multiply_non_integer():
    result = get_interpreter_output("[multiply:4.5;3.5]")
    assert result == "15.75"


def test_add_invalid():
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[add:a;b]")
    assert (
        e_info.value.message
        == "[function_definitions#parse_numbers] invalid numeric argument 'a'"
    )
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[add:3]")
    assert (
        e_info.value.message
        == "[function_definitions#add] add requires at least two numbers"
    )


def test_subtract_invalid():
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[subtract:a;b]")
    assert (
        e_info.value.message
        == "[function_definitions#parse_numbers] invalid numeric argument 'a'"
    )
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[subtract:]")
    assert (
        e_info.value.message
        == "[function_definitions#subtract] subtract requires at least two numbers"
    )


def test_multiply_invalid():
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[multiply:a;b]")
    assert (
        e_info.value.message
        == "[function_definitions#parse_numbers] invalid numeric argument 'a'"
    )
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[multiply:3]")
    assert (
        e_info.value.message
        == "[function_definitions#multiply] multiply requires at least two numbers"
    )
