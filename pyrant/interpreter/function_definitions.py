from interpreter.block_attributes import BlockAttributeManager, BlockAttributes
from .formatting_object import FormattingStrategy
import interpreter.formatter as Formatter
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
            Formatter.set_strategy(FormattingStrategy.NONE)
        case "upper":
            Formatter.set_strategy(FormattingStrategy.UPPER)
        case "lower":
            Formatter.set_strategy(FormattingStrategy.LOWER)
        case "sentence":
            Formatter.set_strategy(FormattingStrategy.SENTENCE)
        case "title":
            Formatter.set_strategy(FormattingStrategy.TITLE)
        case _:
            pass

def rand(args: list[str]) -> str:
    minimum = int(args[0])
    maximum = int(args[1])
    return str(randint(minimum, maximum))

