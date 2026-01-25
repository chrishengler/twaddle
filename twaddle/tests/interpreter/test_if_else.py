from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


def get_interpreter_output(sentence: str) -> str:
    interpreter = Interpreter(LookupManager())
    return interpreter.interpret_external(sentence)


# ============================================================================
# Basic if/else tests with simple predicates
# ============================================================================


def test_if_true_simple():
    assert get_interpreter_output("[if:1;yes;no]") == "yes"


def test_if_false_simple():
    assert get_interpreter_output("[if:0;yes;no]") == "no"


def test_if_positive_number():
    assert (
        get_interpreter_output("[if:5;positive true;positive false]") == "positive true"
    )


def test_if_negative_number():
    assert (
        get_interpreter_output("[if:-3;negative true;negative false]")
        == "negative false"
    )


def test_if_zero():
    assert (
        get_interpreter_output("[if:0;zero is true;zero is false]") == "zero is false"
    )


def test_if_positive_float():
    assert get_interpreter_output("[if:0.5;float true;float false]") == "float true"


def test_if_negative_float():
    assert (
        get_interpreter_output("[if:-0.5;negative float;not negative float]")
        == "not negative float"
    )


def test_if_non_empty_string():
    assert (
        get_interpreter_output("[if:hello;string true;string false]") == "string true"
    )


def test_if_empty_string():
    assert get_interpreter_output("[if:;empty true;empty false]") == "empty false"


def test_if_whitespace_only():
    assert (
        get_interpreter_output("[if:   ;whitespace true;whitespace false]")
        == "whitespace false"
    )


# ============================================================================
# Tests with logical function predicates
# ============================================================================


def test_if_with_bool_function_true():
    assert get_interpreter_output("[if:[bool:5];yes;no]") == "yes"


def test_if_with_bool_function_false():
    assert get_interpreter_output("[if:[bool:0];yes;no]") == "no"


def test_if_with_less_than_true():
    assert get_interpreter_output("[if:[less_than:2;5];less;not less]") == "less"


def test_if_with_less_than_false():
    assert get_interpreter_output("[if:[less_than:5;2];less;not less]") == "not less"


def test_if_with_greater_than_true():
    assert (
        get_interpreter_output("[if:[greater_than:10;3];greater;not greater]")
        == "greater"
    )


def test_if_with_greater_than_false():
    assert (
        get_interpreter_output("[if:[greater_than:2;5];greater;not greater]")
        == "not greater"
    )


def test_if_with_equal_to_true():
    assert get_interpreter_output("[if:[equal_to:5;5];equal;not equal]") == "equal"


def test_if_with_equal_to_false():
    assert get_interpreter_output("[if:[equal_to:5;3];equal;not equal]") == "not equal"


def test_if_with_and_true():
    assert (
        get_interpreter_output("[if:[and:1;1];both true;not both true]") == "both true"
    )


def test_if_with_and_false():
    assert (
        get_interpreter_output("[if:[and:1;0];both true;not both true]")
        == "not both true"
    )


def test_if_with_or_true():
    assert (
        get_interpreter_output("[if:[or:1;0];at least one;neither]") == "at least one"
    )


def test_if_with_or_false():
    assert get_interpreter_output("[if:[or:0;0];at least one;neither]") == "neither"


def test_if_with_not_true():
    assert get_interpreter_output("[if:[not:0];not zero;is zero]") == "not zero"


def test_if_with_not_false():
    assert get_interpreter_output("[if:[not:1];not one;is one]") == "is one"


def test_if_with_xor_true():
    assert get_interpreter_output("[if:[xor:1;0];different;same]") == "different"


def test_if_with_xor_false():
    assert get_interpreter_output("[if:[xor:1;1];different;same]") == "same"


# ============================================================================
# Tests with function calls in branches
# ============================================================================


def test_if_with_function_in_true_branch():
    assert get_interpreter_output("[if:1;[add:2;3];0]") == "5"


def test_if_with_function_in_false_branch():
    assert get_interpreter_output("[if:0;0;[add:2;3]]") == "5"


def test_if_with_functions_in_both_branches():
    result_true = get_interpreter_output("[if:1;[add:2;3];[sub:10;3]]")
    result_false = get_interpreter_output("[if:0;[add:2;3];[sub:10;3]]")
    assert result_true == "5"
    assert result_false == "7"


def test_if_with_string_functions():
    assert get_interpreter_output("[if:1;[reverse]{hello};hello]") == "olleh"
    assert get_interpreter_output("[if:0;[reverse]{hello};hello]") == "hello"


# ============================================================================
# Tests with nested if statements
# ============================================================================


def test_if_nested_in_true_branch():
    sentence = "[if:1;[if:1;inner true;inner false];outer false]"
    assert get_interpreter_output(sentence) == "inner true"


def test_if_nested_in_false_branch():
    sentence = "[if:0;outer true;[if:1;inner true;inner false]]"
    assert get_interpreter_output(sentence) == "inner true"


def test_if_deeply_nested():
    sentence = "[if:1;[if:1;[if:1;deeply true;deep false];mid false];outer false]"
    assert get_interpreter_output(sentence) == "deeply true"


def test_if_nested_with_different_outcomes():
    sentence = "[if:[greater_than:5;3];[if:[less_than:2;4];both;first only];neither]"
    assert get_interpreter_output(sentence) == "both"


# ============================================================================
# Tests with empty branches
# ============================================================================


def test_if_empty_true_branch():
    assert get_interpreter_output("[if:1;;no]") == ""


def test_if_empty_false_branch():
    assert get_interpreter_output("[if:0;yes;]") == ""


def test_if_both_branches_empty():
    assert get_interpreter_output("[if:1;;]") == ""
    assert get_interpreter_output("[if:0;;]") == ""


# ============================================================================
# Integration tests with copy/paste
# ============================================================================


def test_if_with_copy_paste_in_predicate():
    sentence = "[hide]{[copy:var]{5}}[if:[paste:var];yes;no]"
    assert get_interpreter_output(sentence) == "yes"


def test_if_with_copy_paste_in_branches():
    sentence = "[hide]{[copy:val]{10}}[if:1;[paste:val];[add:[paste:val];8]]"
    assert get_interpreter_output(sentence) == "10"


def test_if_selecting_branch_based_on_comparison_with_paste():
    sentence = "[hide]{[copy:x]{3}}[if:[less_than:[paste:x];5];small;large]"
    assert get_interpreter_output(sentence) == "small"


# ============================================================================
# Integration tests with while loops
# ============================================================================


def test_if_inside_while_loop():
    sentence = (
        "[hide]{[copy:i]{0}}[while:[less_than:[paste:i];3]]{[if:[equal_to:[paste:i];1];X;O]"
        "[hide]{[copy:i]{[add:[paste:i];1]}}}"
    )
    assert get_interpreter_output(sentence) == "OXO"


def test_while_loop_inside_if_true_branch():
    sentence = (
        "[hide]{[copy:i]{1}}[if:[paste:i];[while:[less_than:[paste:i];4]]"
        "{{A}[hide]{[copy:i]{[add:[paste:i];1]}}}]"
    )
    assert get_interpreter_output(sentence) == "AAA"


def test_while_loop_inside_if_false_branch():
    sentence = "[if:0; ;[hide]{[copy:i]{0}}[while:[less_than:[paste:i];3]]{B[hide]{[copy:i]{[add:[paste:i];1]}}}]"
    assert get_interpreter_output(sentence) == "BBB"


# ============================================================================
# Edge cases and complex predicates
# ============================================================================


def test_if_with_complex_predicate():
    # ((5 > 2) AND (3 < 10)) -> true
    sentence = (
        "[if:[and:[greater_than:5;2];[less_than:3;10]];complex true;complex false]"
    )
    assert get_interpreter_output(sentence) == "complex true"


def test_if_with_complex_nested_logical_predicates():
    # NOT((1 == 0) OR (5 < 2)) -> NOT(0 OR 0) -> NOT(0) -> 1
    sentence = "[if:[not:[or:[equal_to:1;0];[less_than:5;2]]];logic true;logic false]"
    assert get_interpreter_output(sentence) == "logic true"


def test_if_with_mathematical_predicate():
    # [add:2;3] results in 5, which is truthy
    assert get_interpreter_output("[if:[add:2;3];sum true;sum false]") == "sum true"


def test_if_with_zero_result_predicate():
    # [sub:5;5] results in 0, which is falsy
    assert get_interpreter_output("[if:[sub:5;5];diff true;diff false]") == "diff false"


# ============================================================================
# Tests with special characters and whitespace
# ============================================================================


def test_if_with_whitespace_in_branches():
    assert get_interpreter_output("[if:1;  yes  ;  no  ]") == "  yes  "


def test_if_with_newlines_in_branches():
    # Assuming newlines are preserved in the output
    result = get_interpreter_output("[if:1;line1\nline2;other]")
    assert result == "line1\nline2"


def test_if_with_special_characters():
    assert get_interpreter_output("[if:1;@#$%;^&*()]") == "@#$%"


# ============================================================================
# Tests with multiple if statements in sequence
# ============================================================================


def test_multiple_sequential_ifs():
    sentence = "[if:1;A;B][if:0;C;D][if:1;E;F]"
    assert get_interpreter_output(sentence) == "ADE"


def test_chained_if_else_logic():
    # Simulating if-elif-else with nested ifs
    sentence = "[hide]{[copy:x]{7}}[if:[less_than:[paste:x];5];small;[if:[less_than:[paste:x];10];medium;large]]"
    assert get_interpreter_output(sentence) == "medium"


# ============================================================================
# Tests with rep function integration
# ============================================================================


def test_if_with_rep_in_true_branch():
    assert get_interpreter_output("[if:1;[rep:3]{A};B]") == "AAA"


def test_if_with_rep_in_false_branch():
    assert get_interpreter_output("[if:0;A;[rep:3]{B}]") == "BBB"


def test_if_inside_rep():
    assert get_interpreter_output("[rep:3]{[if:1;X;O]}") == "XXX"


def test_if_alternating_with_counter_in_rep():
    sentence = "[hide]{[copy:i]{0}}[rep:4]{[if:[less_than:[paste:i];2];A;B][hide]{[copy:i]{[add:[paste:i];1]}}}"
    assert get_interpreter_output(sentence) == "AABB"
