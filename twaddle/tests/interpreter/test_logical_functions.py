import pytest

from twaddle.exceptions import TwaddleFunctionException
from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


# ============================================================================
# Tests for [bool:<x>]
# ============================================================================


def test_bool_positive_number():
    assert get_interpreter_output("[bool:5]") == "1"


def test_bool_negative_number():
    assert get_interpreter_output("[bool:-3]") == "0"


def test_bool_zero():
    assert get_interpreter_output("[bool:0]") == "0"


def test_bool_positive_float():
    assert get_interpreter_output("[bool:0.5]") == "1"


def test_bool_negative_float():
    assert get_interpreter_output("[bool:-0.5]") == "0"


def test_bool_non_empty_string():
    assert get_interpreter_output("[bool:hello]") == "1"


def test_bool_empty_string():
    assert get_interpreter_output("[bool:]") == "0"


def test_bool_whitespace_only():
    # Whitespace-only strings after strip would be empty, treated as False
    assert get_interpreter_output("[bool:   ]") == "0"


# ============================================================================
# Tests for [less_than:<x>;<y>]
# ============================================================================


def test_less_than_true():
    assert get_interpreter_output("[less_than:2;5]") == "1"


def test_less_than_false():
    assert get_interpreter_output("[less_than:5;2]") == "0"


def test_less_than_equal():
    assert get_interpreter_output("[less_than:5;5]") == "0"


def test_less_than_negative():
    assert get_interpreter_output("[less_than:-10;-5]") == "1"


def test_less_than_negative_and_positive():
    assert get_interpreter_output("[less_than:-5;3]") == "1"


def test_less_than_float():
    assert get_interpreter_output("[less_than:2.5;3.7]") == "1"


def test_less_than_mixed_int_float():
    assert get_interpreter_output("[less_than:2;3.5]") == "1"


def test_less_than_invalid_first_arg():
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[less_than:abc;5]")
    assert (
        str(e_info.value)
        == "[function_definitions#parse_numbers] invalid numeric argument 'abc'"
    )


def test_less_than_invalid_second_arg():
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[less_than:5;xyz]")
    assert (
        str(e_info.value)
        == "[function_definitions#parse_numbers] invalid numeric argument 'xyz'"
    )


# ============================================================================
# Tests for [greater_than:<x>;<y>]
# ============================================================================


def test_greater_than_true():
    assert get_interpreter_output("[greater_than:5;2]") == "1"


def test_greater_than_false():
    assert get_interpreter_output("[greater_than:2;5]") == "0"


def test_greater_than_equal():
    assert get_interpreter_output("[greater_than:5;5]") == "0"


def test_greater_than_negative():
    assert get_interpreter_output("[greater_than:-5;-10]") == "1"


def test_greater_than_negative_and_positive():
    assert get_interpreter_output("[greater_than:3;-5]") == "1"


def test_greater_than_float():
    assert get_interpreter_output("[greater_than:3.7;2.5]") == "1"


def test_greater_than_mixed_int_float():
    assert get_interpreter_output("[greater_than:3.5;2]") == "1"


def test_greater_than_invalid_first_arg():
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[greater_than:abc;5]")
    assert (
        str(e_info.value)
        == "[function_definitions#parse_numbers] invalid numeric argument 'abc'"
    )


def test_greater_than_invalid_second_arg():
    with pytest.raises(TwaddleFunctionException) as e_info:
        get_interpreter_output("[greater_than:5;xyz]")
    assert (
        str(e_info.value)
        == "[function_definitions#parse_numbers] invalid numeric argument 'xyz'"
    )


# ============================================================================
# Tests for [equal_to:<x>;<y>]
# ============================================================================


def test_equal_to_numeric_true():
    assert get_interpreter_output("[equal_to:5;5]") == "1"


def test_equal_to_numeric_false():
    assert get_interpreter_output("[equal_to:5;3]") == "0"


def test_equal_to_float():
    assert get_interpreter_output("[equal_to:3.5;3.5]") == "1"


def test_equal_to_float_false():
    assert get_interpreter_output("[equal_to:3.5;3.6]") == "0"


def test_equal_to_negative():
    assert get_interpreter_output("[equal_to:-5;-5]") == "1"


def test_equal_to_string_true():
    assert get_interpreter_output("[equal_to:hello;hello]") == "1"


def test_equal_to_string_false():
    assert get_interpreter_output("[equal_to:hello;world]") == "0"


def test_equal_to_mixed_string_number():
    # One is numeric, one is not: string comparison
    assert get_interpreter_output("[equal_to:5;hello]") == "0"


def test_equal_to_numeric_zero():
    assert get_interpreter_output("[equal_to:0;0]") == "1"


def test_equal_to_numeric_zero_vs_negative():
    assert get_interpreter_output("[equal_to:0;-0]") == "1"


def test_equal_to_empty_strings():
    assert get_interpreter_output("[equal_to:;]") == "1"


# ============================================================================
# Tests for [and:<x>;<y>]
# ============================================================================


def test_and_true_true():
    assert get_interpreter_output("[and:1;1]") == "1"


def test_and_true_false():
    assert get_interpreter_output("[and:1;0]") == "0"


def test_and_false_true():
    assert get_interpreter_output("[and:0;1]") == "0"


def test_and_false_false():
    assert get_interpreter_output("[and:0;0]") == "0"


def test_and_positive_numbers():
    assert get_interpreter_output("[and:5;3]") == "1"


def test_and_zero_and_positive():
    assert get_interpreter_output("[and:0;5]") == "0"


def test_and_negative_numbers():
    assert get_interpreter_output("[and:-1;-2]") == "0"


def test_and_strings_both_nonempty():
    assert get_interpreter_output("[and:hello;world]") == "1"


def test_and_string_empty_and_nonempty():
    assert get_interpreter_output("[and:;hello]") == "0"


def test_and_mixed_string_number():
    assert get_interpreter_output("[and:5;hello]") == "1"


# ============================================================================
# Tests for [not:<x>]
# ============================================================================


def test_not_true():
    assert get_interpreter_output("[not:1]") == "0"


def test_not_false():
    assert get_interpreter_output("[not:0]") == "1"


def test_not_positive_number():
    assert get_interpreter_output("[not:5]") == "0"


def test_not_negative_number():
    assert get_interpreter_output("[not:-3]") == "1"


def test_not_zero():
    assert get_interpreter_output("[not:0]") == "1"


def test_not_nonempty_string():
    assert get_interpreter_output("[not:hello]") == "0"


def test_not_empty_string():
    assert get_interpreter_output("[not:]") == "1"


# ============================================================================
# Tests for [or:<x>;<y>]
# ============================================================================


def test_or_true_true():
    assert get_interpreter_output("[or:1;1]") == "1"


def test_or_true_false():
    assert get_interpreter_output("[or:1;0]") == "1"


def test_or_false_true():
    assert get_interpreter_output("[or:0;1]") == "1"


def test_or_false_false():
    assert get_interpreter_output("[or:0;0]") == "0"


def test_or_positive_numbers():
    assert get_interpreter_output("[or:5;3]") == "1"


def test_or_zero_and_positive():
    assert get_interpreter_output("[or:0;5]") == "1"


def test_or_zero_and_zero():
    assert get_interpreter_output("[or:0;0]") == "0"


def test_or_negative_numbers():
    assert get_interpreter_output("[or:-1;-2]") == "0"


def test_or_strings_both_nonempty():
    assert get_interpreter_output("[or:hello;world]") == "1"


def test_or_string_empty_and_nonempty():
    assert get_interpreter_output("[or:;hello]") == "1"


def test_or_both_empty():
    assert get_interpreter_output("[or:;]") == "0"


# ============================================================================
# Tests for [xor:<x>;<y>]
# ============================================================================


def test_xor_true_true():
    assert get_interpreter_output("[xor:1;1]") == "0"


def test_xor_true_false():
    assert get_interpreter_output("[xor:1;0]") == "1"


def test_xor_false_true():
    assert get_interpreter_output("[xor:0;1]") == "1"


def test_xor_false_false():
    assert get_interpreter_output("[xor:0;0]") == "0"


def test_xor_positive_numbers():
    assert get_interpreter_output("[xor:5;3]") == "0"


def test_xor_zero_and_positive():
    assert get_interpreter_output("[xor:0;5]") == "1"


def test_xor_zero_and_zero():
    assert get_interpreter_output("[xor:0;0]") == "0"


def test_xor_negative_numbers():
    assert get_interpreter_output("[xor:-1;-2]") == "0"


def test_xor_strings_both_nonempty():
    assert get_interpreter_output("[xor:hello;world]") == "0"


def test_xor_string_empty_and_nonempty():
    assert get_interpreter_output("[xor:;hello]") == "1"


def test_xor_both_empty():
    assert get_interpreter_output("[xor:;]") == "0"


# ============================================================================
# Integration tests combining multiple logical functions
# ============================================================================


def test_combination_and_or():
    # (5 < 10) AND (3 > 2) -> "1" AND "1" -> "1"
    result = get_interpreter_output("[and:[less_than:5;10];[greater_than:3;2]]")
    assert result == "1"


def test_combination_not_equal():
    # NOT (5 == 3) -> NOT "0" -> "1"
    result = get_interpreter_output("[not:[equal_to:5;3]]")
    assert result == "1"


def test_combination_xor_and():
    # (5 < 10) XOR (3 > 10) -> "1" XOR "0" -> "1"
    result = get_interpreter_output("[xor:[less_than:5;10];[greater_than:3;10]]")
    assert result == "1"


def test_combination_complex():
    # ((5 > 2) OR (0 == 1)) AND NOT(0)
    # ("1" OR "0") AND "1" -> "1" AND "1" -> "1"
    result = get_interpreter_output(
        "[and:[or:[greater_than:5;2];[equal_to:0;1]];[not:0]]"
    )
    assert result == "1"
