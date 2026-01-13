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
    repetitions = int(evaluated_args[0])
    block_attribute_manager.current_attributes.repetitions = repetitions


def separator(
    _evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    raw_args: list[RootObject],
):
    block_attribute_manager.current_attributes.separator = raw_args[0]


def first(
    _evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    raw_args: list[RootObject],
):
    block_attribute_manager.current_attributes.first = raw_args[0]


def last(
    _evaluated_args,
    block_attribute_manager: BlockAttributeManager,
    raw_args: list[RootObject],
):
    block_attribute_manager.current_attributes.last = raw_args[0]


def save(
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
):
    block_attribute_manager.save_block(evaluated_args[0])


def copy(
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
):
    block_attribute_manager.copy_block(evaluated_args[0])


def sync(
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
):
    block_attribute_manager.set_synchronizer(evaluated_args)


def abbreviate(
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
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


def case(evaluated_args: list[str], _block_attribute_manager, _raw_args):
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
def match(evaluated_args: list[str], _block_attribute_manager, _raw_args):
    return RegexState.match


def rand(evaluated_args: list[str], _block_attribute_manager, _raw_args) -> str:
    minimum = int(evaluated_args[0])
    maximum = int(evaluated_args[1])
    return str(randint(minimum, maximum))


def reverse(_evaluated_args: list[str], block_attribute_manager, _raw_args):
    block_attribute_manager.current_attributes.reverse = True


def hide(
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
) -> str:
    block_attribute_manager.current_attributes.hidden = True


def add(
    evaluated_args: list[str],
    block_attribute_manager: BlockAttributeManager,
    _raw_args,
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
    _raw_args,
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
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
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
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
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
