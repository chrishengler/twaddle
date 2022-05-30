from interpreter.block_attributes import BlockAttributeManager
from .formatting_object import FormattingStrategy
import interpreter.formatter as formatter
from .regex_state import RegexState
from random import randint


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
            formatter.set_strategy(FormattingStrategy.NONE)
        case "upper":
            formatter.set_strategy(FormattingStrategy.UPPER)
        case "lower":
            formatter.set_strategy(FormattingStrategy.LOWER)
        case "sentence":
            formatter.set_strategy(FormattingStrategy.SENTENCE)
        case "title":
            formatter.set_strategy(FormattingStrategy.TITLE)
        case _:
            pass


# noinspection PyUnusedLocal
def match(args: list[str]):
    return RegexState.match


def rand(args: list[str]) -> str:
    minimum = int(args[0])
    maximum = int(args[1])
    return str(randint(minimum, maximum))
