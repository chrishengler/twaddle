from interpreter.block_attributes import BlockAttributeManager, BlockAttributes
from random import randint


def repeat(args: list[str]):
    repetitions = int(args[0])
    BlockAttributeManager.current_attributes.repetitions = repetitions


def separator(args: list[str]):
    BlockAttributeManager.current_attributes.separator = args[0]


def rand(args: list[str]) -> str:
    minimum = int(args[0])
    maximum = int(args[1])
    return str(randint(minimum, maximum))

