from math import prod
from random import randint
from typing import Optional

from twaddle.compiler.compiler_objects import RootObject
from twaddle.exceptions import TwaddleFunctionException
from twaddle.interpreter.block_attributes import BlockAttributeManager
from twaddle.interpreter.formatting_object import FormattingStrategy
from twaddle.interpreter.regex_state import RegexState


def _parse_numbers(args: list[str]) -> list[int | float]:
    results: list[int | float] = []
    for raw in args:
        s = raw.strip()
        if s == "":
            raise TwaddleFunctionException(
                "[function_definitions#parse_numbers] invalid numeric argument ''"
            )
        if s.lstrip("+-").isdigit():
            results.append(int(s))
            continue
        try:
            results.append(float(s))
        except ValueError:
            raise TwaddleFunctionException(
                f"[function_definitions#parse_numbers] invalid numeric argument '{s}'"
            )
    return results


def _format_number(value: int | float, max_decimals: Optional[int]) -> str:
    """Format a numeric value using at most `max_decimals` decimal places.

    - Integers are returned without a decimal point.
    - If `max_decimals` is None, default to 3 decimals.
    - If `max_decimals` is 0 or negative, return the rounded integer part.
    - For floats, round to `max_decimals` places and trim trailing zeros
      and any trailing decimal point.
    """
    if isinstance(value, int):
        return str(value)

    # Default to 3 decimals when not specified
    if max_decimals is None:
        max_decimals = 3

    if max_decimals <= 0:
        return str(int(round(value)))

    formatted = f"{value:.{max_decimals}f}"
    formatted = formatted.rstrip("0").rstrip(".")
    return formatted if formatted != "" else "0"


def repeat(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#repeat] repeat requires exactly one argument"
        )
    repetitions = int(evaluated_args[0])
    block_attribute_manager.current_attributes.repetitions = repetitions


def separator(
    _evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    raw_args: list[RootObject],
):
    if len(raw_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#separator] separator requires exactly one argument"
        )
    block_attribute_manager.current_attributes.separator = raw_args[0]


def first(
    _evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    raw_args: list[RootObject],
):
    if len(raw_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#first] first requires exactly one argument"
        )
    block_attribute_manager.current_attributes.first = raw_args[0]


def last(
    _evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    raw_args: list[RootObject],
):
    if len(raw_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#last] last requires exactly one argument"
        )
    block_attribute_manager.current_attributes.last = raw_args[0]


def save(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#save] save requires exactly one argument"
        )
    block_attribute_manager.save_block(evaluated_args[0])


def copy(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#copy] copy requires exactly one argument"
        )
    block_attribute_manager.copy_block(evaluated_args[0])


def sync(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#sync] sync requires at least one argument"
        )
    block_attribute_manager.set_synchronizer(evaluated_args)


def abbreviate(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    block_attribute_manager.current_attributes.abbreviate = True
    if len(evaluated_args) == 0:
        block_attribute_manager.current_attributes.abbreviation_case = (
            FormattingStrategy.UPPER
        )
        return
    case = evaluated_args[0].strip().lower()
    match case:
        case "retain":
            block_attribute_manager.current_attributes.abbreviation_case = (
                FormattingStrategy.NONE
            )
        case "upper":
            block_attribute_manager.current_attributes.abbreviation_case = (
                FormattingStrategy.UPPER
            )
        case "lower":
            block_attribute_manager.current_attributes.abbreviation_case = (
                FormattingStrategy.LOWER
            )
        case "first":
            block_attribute_manager.current_attributes.abbreviation_case = (
                FormattingStrategy.TITLE
            )
        case _:
            raise TwaddleFunctionException(
                "[function_definitions#abbreviate] invalid case " f"argument '{case}'"
            )


def case(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#case] case requires exactly one argument"
        )
    arg = evaluated_args[0].strip().lower()
    match arg:
        case "none":
            return FormattingStrategy.NONE
        case "upper":
            return FormattingStrategy.UPPER
        case "lower":
            return FormattingStrategy.LOWER
        case "sentence":
            return FormattingStrategy.SENTENCE
        case "title":
            return FormattingStrategy.TITLE
        case _:
            pass


# noinspection PyUnusedLocal
def match(
    _evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    return RegexState.match


def rand(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#rand] rand requires exactly two arguments"
        )
    minimum = int(evaluated_args[0])
    maximum = int(evaluated_args[1])
    return str(randint(minimum, maximum))


def reverse(
    _evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    block_attribute_manager.current_attributes.reverse = True


def hide(
    _evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    block_attribute_manager.current_attributes.hidden = True
    return ""


def add(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 2:
        raise TwaddleFunctionException(
            "[function_definitions#add] add requires at least two numbers"
        )
    parsed_numbers = _parse_numbers(evaluated_args)
    return _format_number(
        sum(parsed_numbers), block_attribute_manager.current_attributes.max_decimals
    )


def subtract(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 2:
        raise TwaddleFunctionException(
            "[function_definitions#subtract] subtract requires at least two numbers"
        )
    parsed_numbers = _parse_numbers(evaluated_args)
    parsed_numbers = [parsed_numbers[0]] + [-value for value in parsed_numbers[1:]]
    return _format_number(
        sum(parsed_numbers), block_attribute_manager.current_attributes.max_decimals
    )


def multiply(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) < 2:
        raise TwaddleFunctionException(
            "[function_definitions#multiply] multiply requires at least two numbers"
        )
    parsed_numbers = _parse_numbers(evaluated_args)
    return _format_number(
        prod(parsed_numbers), block_attribute_manager.current_attributes.max_decimals
    )


def divide(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
):
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#divide] divide requires exactly two numbers"
        )
    parsed_numbers = _parse_numbers(evaluated_args)
    if parsed_numbers[1] == 0:
        raise TwaddleFunctionException(
            "[function_definitions#divide] cannot divide by zero"
        )
    return _format_number(
        parsed_numbers[0] / parsed_numbers[1],
        block_attribute_manager.current_attributes.max_decimals,
    )


def boolean_helper(evaluated_arg: str) -> bool:
    try:
        as_number = _parse_numbers([evaluated_arg])
        return True if as_number[0] > 0 else False
    except TwaddleFunctionException:
        return True if len(evaluated_arg.strip()) else False


def boolean(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 1:
        raise TwaddleFunctionException(
            "[function_definitions#bool] bool requires exactly one argument"
        )
    converted = boolean_helper(evaluated_args[0])
    return "1" if converted else "0"


def less_than(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#less_than] less_than requires exactly two arguments"
        )
    args_as_numbers = _parse_numbers(evaluated_args)
    return "1" if (args_as_numbers[0] < args_as_numbers[1]) else "0"


def greater_than(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#less_than] less_than requires exactly two arguments"
        )
    args_as_numbers = _parse_numbers(evaluated_args)
    return "1" if (args_as_numbers[0] > args_as_numbers[1]) else "0"


def equal_to(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#equal_to] equal_to requires exactly two arguments"
        )
    try:
        args_as_numbers = _parse_numbers(evaluated_args)
        return "1" if (args_as_numbers[0] == args_as_numbers[1]) else "0"
    except TwaddleFunctionException:
        return "1" if (evaluated_args[0].strip() == evaluated_args[1].strip()) else "0"


def logical_and(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#logical_and] logical_and requires exactly two arguments"
        )
    args = [boolean_helper(arg) for arg in evaluated_args]
    return "1" if (args[0] and args[1]) else "0"


def logical_not(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 1:
        raise TwaddleFunctionException(
            "[function_definitions#logical_not] logical_not requires exactly one argument"
        )
    converted = boolean_helper(evaluated_args[0])
    return "0" if converted else "1"


def logical_or(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#logical_or] logical_or requires exactly two arguments"
        )
    args = [boolean_helper(arg) for arg in evaluated_args]
    return "1" if (args[0] or args[1]) else "0"


def logical_xor(
    evaluated_args: list[str],
    _block_attribute_manager: BlockAttributeManager,
    _raw_args: list[RootObject],
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#logical_or] logical_or requires exactly two arguments"
        )
    args = [boolean_helper(arg) for arg in evaluated_args]
    return "1" if (args[0] != args[1]) else "0"


def while_loop(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    raw_args: list[RootObject],
):
    if len(raw_args) not in [1, 2]:
        raise TwaddleFunctionException(
            f"[function_definitions#while] while requires either one or two arguments, got {len(raw_args)}"
        )
    if len(evaluated_args) == 2:
        try:
            max_iterations = _parse_numbers([evaluated_args[1]])[0]
            if not isinstance(max_iterations, int):
                raise TwaddleFunctionException(
                    "[function_definitions#while] max iterations must be int,"
                    f" got {raw_args[1]}, evaluated to {evaluated_args[1]}"
                )
            block_attribute_manager.current_attributes.max_while_iterations = (
                max_iterations
            )
        except TwaddleFunctionException:
            raise TwaddleFunctionException(
                "[function_definitions#while] max iterations must be int,"
                f" got {raw_args[1]}, evaluated to {evaluated_args[1]}"
            )

    block_attribute_manager.current_attributes.while_predicate = raw_args[0]
