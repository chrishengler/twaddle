from random import randint

from twaddle.interpreter.block_attributes import BlockAttributeManager

from .formatting_object import FormattingStrategy
from .regex_state import RegexState


def repeat(args: list[str]):
    repetitions = int(args[0])
    BlockAttributeManager.current_attributes.repetitions = repetitions


def separator(args: list[str]):
    BlockAttributeManager.current_attributes.separator = args[0]


def first(args: list[str]):
    BlockAttributeManager.current_attributes.first = args[0]


def last(args: list[str]):
    BlockAttributeManager.current_attributes.last = args[0]


def sync(args: list[str]):
    BlockAttributeManager.set_synchronizer(args)


def case(args: list[str]):
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
def match(args: list[str]):
    return RegexState.match


def rand(args: list[str]) -> str:
    minimum = int(args[0])
    maximum = int(args[1])
    return str(randint(minimum, maximum))
