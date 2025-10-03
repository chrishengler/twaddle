from random import randint

from twaddle.compiler.compiler_objects import RootObject
from twaddle.exceptions import TwaddleFunctionException
from twaddle.interpreter.block_attributes import BlockAttributeManager
from twaddle.interpreter.formatting_object import FormattingStrategy
from twaddle.interpreter.regex_state import RegexState


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
