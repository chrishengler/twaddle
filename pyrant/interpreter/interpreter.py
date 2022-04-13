from parser.rant_object import *
from random import randrange


def interpret(parse_result: list[RantObject]) -> str:
    result: str = ""

    for obj in parse_result:
        match obj.type:
            case RantObjectType.TEXT:
                result += obj.text
            case RantObjectType.BLOCK:
                result += handle_block(obj)
            case _:
                continue
    return result


def handle_block(block: RantBlockObject) -> str:
    return interpret(block.choices[randrange(0, len(block.choices))])
