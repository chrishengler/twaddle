from random import randint

from twaddle.compiler.compiler_objects import RootObject
from twaddle.interpreter.block_attributes import BlockAttributeManager

from .formatting_object import FormattingStrategy
from .regex_state import RegexState


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


def sync(
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
):
    block_attribute_manager.set_synchronizer(evaluated_args)


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


def hide(
    evaluated_args: list[str], block_attribute_manager: BlockAttributeManager, _raw_args
) -> str:
    block_attribute_manager.current_attributes.hidden = True
