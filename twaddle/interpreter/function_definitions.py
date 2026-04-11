from math import prod
from random import randint
from typing import Optional

from twaddle.exceptions import TwaddleFunctionException
from twaddle.interpreter.context import TwaddleContext

# from twaddle.interpreter.formatter import Formatter
from twaddle.interpreter.formatting_object import FormattingStrategy
from twaddle.interpreter.function_registry import FunctionRegistry, evaluate_args
from twaddle.interpreter.interpreter_decorator_protocol import (
    InterpreterDecoratorProtocol,
)
from twaddle.parser.nodes import RootNode


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


@FunctionRegistry.register(
    name="repeat",
    aliases=["rep"],
    min_args=1,
    max_args=1,
    description=(
        "A block function. Takes one argument, `n`. "
        "Causes the next block to be opened to be repeated `n` times."
    ),
)
@evaluate_args
def repeat(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#repeat] repeat requires exactly one argument"
        )
    repetitions = int(evaluated_args[0])
    context.block_attributes.repetitions = repetitions


@FunctionRegistry.register(
    name="separator",
    aliases=["sep"],
    min_args=1,
    max_args=1,
    description=(
        "A block function. Takes one argument, `content`. "
        "Sets the content to be placed between repetitions of the next block."
    ),
)
def separator(
    raw_args: list[RootNode],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(raw_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#separator] separator requires exactly one argument"
        )
    context.block_attributes.separator = raw_args[0]


@FunctionRegistry.register(
    name="first",
    min_args=1,
    max_args=1,
    description=(
        "A block function. Takes one argument, `content`. "
        "Sets the content to be placed before the first repetition of the next block."
    ),
)
def first(
    raw_args: list[RootNode],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(raw_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#first] first requires exactly one argument"
        )
    context.block_attributes.first = raw_args[0]


@FunctionRegistry.register(
    name="last",
    min_args=1,
    max_args=1,
    description=(
        "A block function. Takes one argument, `content`. "
        "Sets the content to be placed after the last repetition of the next block."
    ),
)
def last(
    raw_args: list[RootNode],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(raw_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#last] last requires exactly one argument"
        )
    context.block_attributes.last = raw_args[0]


@FunctionRegistry.register(
    name="save",
    min_args=1,
    max_args=1,
    description=(
        "A block function. Takes one argument, `name`. "
        "Saves the pattern of the next block for later retrieval with `load`."
    ),
)
@evaluate_args
def save(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#save] save requires exactly one argument"
        )
    context.block_attributes.save_as = evaluated_args[0]


@FunctionRegistry.register(
    name="copy",
    min_args=1,
    max_args=1,
    description=(
        "A block function. Takes one argument, `name`. "
        "Copies the evaluated output of the next block for later retrieval with `paste`."
    ),
)
@evaluate_args
def copy(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#copy] copy requires exactly one argument"
        )
    context.block_attributes.copy_as = evaluated_args[0]


@FunctionRegistry.register(
    name="sync",
    aliases=["x"],
    min_args=1,
    max_args=2,
    description=(
        "A block function. Takes one or two arguments. "
        "First argument `name` is always required; second argument 'type' (one of: locked, cdeck, deck) "
        "required on first usage and ignored afterwards. "
        "Synchronises the next block's choice with other blocks sharing the same synchroniser name."
    ),
)
@evaluate_args
def sync(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(evaluated_args) < 1:
        raise TwaddleFunctionException(
            "[function_definitions#sync] sync requires at least one argument"
        )
    context.block_attributes.set_synchronizer(evaluated_args)


@FunctionRegistry.register(
    name="abbreviate",
    aliases=["abbr"],
    min_args=0,
    max_args=1,
    description=(
        "A block function. Takes one optional argument, `case` (one of: retain, upper, lower, first). "
        "Abbreviates the output of the next block to its initials, in appropriate case (default: upper)."
    ),
)
@evaluate_args
def abbreviate(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    context.block_attributes.abbreviate = True
    if len(evaluated_args) == 0:
        context.block_attributes.abbreviation_case = FormattingStrategy.UPPER
        return
    case = evaluated_args[0].strip().lower()
    match case:
        case "retain":
            context.block_attributes.abbreviation_case = FormattingStrategy.NONE
        case "upper":
            context.block_attributes.abbreviation_case = FormattingStrategy.UPPER
        case "lower":
            context.block_attributes.abbreviation_case = FormattingStrategy.LOWER
        case "first":
            context.block_attributes.abbreviation_case = FormattingStrategy.TITLE
        case _:
            raise TwaddleFunctionException(
                "[function_definitions#abbreviate] invalid case " f"argument '{case}'"
            )


@FunctionRegistry.register(
    name="case",
    min_args=1,
    max_args=1,
    description=(
        "Takes one argument, `case` (one of: none, upper, lower, sentence, title). "
        "Sets a casing style to be used until the next use of [case]"
    ),
)
@evaluate_args
def case(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
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


@FunctionRegistry.register(
    name="match",
    min_args=0,
    max_args=0,
    description="Takes no arguments. Returns the current regex match, or an empty string if none.",
)
# noinspection PyUnusedLocal
def match(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    return context.current_regex_match if context.current_regex_match else ""


@FunctionRegistry.register(
    name="rand",
    min_args=2,
    max_args=2,
    description="Takes two arguments, `min` and `max`. Returns a random integer between `min` and `max` inclusive.",
)
@evaluate_args
def rand(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#rand] rand requires exactly two arguments"
        )
    minimum = int(evaluated_args[0])
    maximum = int(evaluated_args[1])
    return str(randint(minimum, maximum))


@FunctionRegistry.register(
    name="reverse",
    min_args=0,
    max_args=0,
    description="A block function. Takes no arguments. Causes the result of the next block to be printed in reverse.",
)
def reverse(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    context.block_attributes.reverse = True


@FunctionRegistry.register(
    name="hide",
    min_args=0,
    max_args=0,
    description="A block function. Takes no arguments. Causes the next block to be evaluated but not printed.",
)
def hide(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    context.block_attributes.hidden = True
    return ""


@FunctionRegistry.register(
    name="add",
    min_args=2,
    description="Takes two or more arguments, each a number. Returns their sum.",
)
@evaluate_args
def add(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(evaluated_args) < 2:
        raise TwaddleFunctionException(
            "[function_definitions#add] add requires at least two numbers"
        )
    parsed_numbers = _parse_numbers(evaluated_args)
    return _format_number(sum(parsed_numbers), context.block_attributes.max_decimals)


@FunctionRegistry.register(
    name="subtract",
    aliases=["sub"],
    min_args=2,
    description=(
        "Takes two or more arguments, each a number. "
        "Subtracts all subsequent arguments from the first and returns the result."
    ),
)
@evaluate_args
def subtract(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(evaluated_args) < 2:
        raise TwaddleFunctionException(
            "[function_definitions#subtract] subtract requires at least two numbers"
        )
    parsed_numbers = _parse_numbers(evaluated_args)
    parsed_numbers = [parsed_numbers[0]] + [-value for value in parsed_numbers[1:]]
    return _format_number(sum(parsed_numbers), context.block_attributes.max_decimals)


@FunctionRegistry.register(
    name="multiply",
    aliases=["mul", "prod"],
    min_args=2,
    description="Takes two or more arguments, each a number. Returns their product.",
)
@evaluate_args
def multiply(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(evaluated_args) < 2:
        raise TwaddleFunctionException(
            "[function_definitions#multiply] multiply requires at least two numbers"
        )
    parsed_numbers = _parse_numbers(evaluated_args)
    return _format_number(prod(parsed_numbers), context.block_attributes.max_decimals)


@FunctionRegistry.register(
    name="divide",
    aliases=["div"],
    min_args=2,
    max_args=2,
    description="Takes two arguments, `dividend` and `divisor`. Returns the result of dividing dividend by divisor.",
)
@evaluate_args
def divide(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
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
        context.block_attributes.max_decimals,
    )


def boolean_helper(evaluated_arg: str) -> bool:
    try:
        as_number = _parse_numbers([evaluated_arg])
        return True if as_number[0] > 0 else False
    except TwaddleFunctionException:
        return True if len(evaluated_arg.strip()) else False


@FunctionRegistry.register(
    name="boolean",
    aliases=["bool"],
    min_args=1,
    max_args=1,
    description="Takes one argument, `value`. Returns '1' if the value is truthy, '0' otherwise.",
)
@evaluate_args
def boolean(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 1:
        raise TwaddleFunctionException(
            "[function_definitions#bool] bool requires exactly one argument"
        )
    converted = boolean_helper(evaluated_args[0])
    return "1" if converted else "0"


@FunctionRegistry.register(
    name="less_than",
    aliases=["lt"],
    min_args=2,
    max_args=2,
    description="Takes two arguments, `a` and `b`, which must both be numbers. Returns '1' if a < b, '0' otherwise.",
)
@evaluate_args
def less_than(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#less_than] less_than requires exactly two arguments"
        )
    args_as_numbers = _parse_numbers(evaluated_args)
    return "1" if (args_as_numbers[0] < args_as_numbers[1]) else "0"


@FunctionRegistry.register(
    name="greater_than",
    aliases=["gt"],
    min_args=2,
    max_args=2,
    description="Takes two arguments, `a` and `b`, which must both be numbers. Returns '1' if a > b, '0' otherwise.",
)
@evaluate_args
def greater_than(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#less_than] less_than requires exactly two arguments"
        )
    args_as_numbers = _parse_numbers(evaluated_args)
    return "1" if (args_as_numbers[0] > args_as_numbers[1]) else "0"


@FunctionRegistry.register(
    name="equal_to",
    aliases=["eq"],
    min_args=2,
    max_args=2,
    description=(
        "Takes two arguments, `a` and `b`. Returns '1' if a equals b, '0' otherwise. "
        "Compares numerically if both arguments interpretable as numbers, otherwise string comparison."
    ),
)
@evaluate_args
def equal_to(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
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


@FunctionRegistry.register(
    name="and",
    min_args=2,
    max_args=2,
    description="Takes two arguments, `a` and `b`. Returns '1' if both are truthy, '0' otherwise.",
)
@evaluate_args
def logical_and(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#logical_and] logical_and requires exactly two arguments"
        )
    args = [boolean_helper(arg) for arg in evaluated_args]
    return "1" if (args[0] and args[1]) else "0"


@FunctionRegistry.register(
    name="not",
    min_args=1,
    max_args=1,
    description="Takes one argument, `value`. Returns '1' if the value is falsy, '0' otherwise.",
)
@evaluate_args
def logical_not(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 1:
        raise TwaddleFunctionException(
            "[function_definitions#logical_not] logical_not requires exactly one argument"
        )
    converted = boolean_helper(evaluated_args[0])
    return "0" if converted else "1"


@FunctionRegistry.register(
    name="or",
    min_args=2,
    max_args=2,
    description="Takes two arguments, `a` and `b`. Returns '1' if either is truthy, '0' otherwise.",
)
@evaluate_args
def logical_or(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#logical_or] logical_or requires exactly two arguments"
        )
    args = [boolean_helper(arg) for arg in evaluated_args]
    return "1" if (args[0] or args[1]) else "0"


@FunctionRegistry.register(
    name="xor",
    min_args=2,
    max_args=2,
    description="Takes two arguments, `a` and `b`. Returns '1' if exactly one is truthy, '0' otherwise.",
)
@evaluate_args
def logical_xor(
    evaluated_args: list[str],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
) -> str:
    if len(evaluated_args) != 2:
        raise TwaddleFunctionException(
            "[function_definitions#logical_or] logical_or requires exactly two arguments"
        )
    args = [boolean_helper(arg) for arg in evaluated_args]
    return "1" if (args[0] != args[1]) else "0"


@FunctionRegistry.register(
    name="while",
    min_args=1,
    max_args=2,
    description=(
        "A block function. Takes one or two arguments, `predicate` and optionally `max_iterations` (must be"
        "interpretable as int). "
        "Repeats the next block while the predicate evaluates to truthy, stopping after at most"
        "`max_iterations` (default: 100)."
    ),
)
def while_loop(
    raw_args: list[RootNode],
    context: TwaddleContext,
    interpreter: InterpreterDecoratorProtocol,
):
    if len(raw_args) not in [1, 2]:
        raise TwaddleFunctionException(
            f"[function_definitions#while] while requires either one or two arguments, got {len(raw_args)}"
        )
    if len(raw_args) == 2:
        max_iterations = _parse_numbers([interpreter.evaluate(raw_args[1])])[0]
        if not isinstance(max_iterations, int):
            raise TwaddleFunctionException(
                "[function_definitions#while] max iterations must be int,"
                f" got {raw_args[1]}, evaluated to {max_iterations}"
            )
        context.block_attributes.max_while_iterations = max_iterations

    context.block_attributes.while_predicate = raw_args[0]
