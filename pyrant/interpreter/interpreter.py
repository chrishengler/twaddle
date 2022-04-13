import lexer.rant_lexer as Lexer
import parser.rant_parser as Parser
from parser.rant_object import *
from random import randrange


def interpret_external(sentence: str) -> str:
    return interpret_internal(Parser.parse(Lexer.lex(sentence)))


def interpret_internal(parse_result: list[RantObject]) -> str:
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
    return interpret_internal(block.choices[randrange(0, len(block.choices))])
