from random import randint

from twaddle.interpreter.block_attributes import BlockAttributeManager

from .formatting_object import FormattingStrategy
from .regex_state import RegexState


def repeat(args: list[str], block_attribute_manager: BlockAttributeManager):
    repetitions = int(args[0])
    block_attribute_manager.current_attributes.repetitions = repetitions


def separator(args: list[str], block_attribute_manager: BlockAttributeManager):
    block_attribute_manager.current_attributes.separator = args[0]


def first(args: list[str], block_attribute_manager: BlockAttributeManager):
    block_attribute_manager.current_attributes.first = args[0]


def last(args: list[str], block_attribute_manager: BlockAttributeManager):
    block_attribute_manager.current_attributes.last = args[0]


def sync(args: list[str], block_attribute_manager: BlockAttributeManager):
    block_attribute_manager.set_synchronizer(args)


def case(args: list[str], _block_attribute_manager):
    arg = args[0].strip().lower()
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
def match(args: list[str], _block_attribute_manager):
    return RegexState.match


def rand(args: list[str], _block_attribute_manager) -> str:
    minimum = int(args[0])
    maximum = int(args[1])
    return str(randint(minimum, maximum))
