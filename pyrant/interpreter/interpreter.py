import lexer.rant_lexer as Lexer
import parser.rant_parser as Parser
from .function_dict import function_definitions
from .block_attributes import BlockAttributeManager, BlockAttributes

from collections import deque
from functools import singledispatch
from parser.rant_object import *
from random import randrange


def interpret_external(sentence: str) -> str:
    return interpret_internal(Parser.parse(Lexer.lex(sentence)))


def interpret_internal(parse_result: deque[RantObject]) -> str:
    result: str = ""

    for obj in parse_result:
        obj_result = run(obj)
        if obj_result is not None:
            result += obj_result
    return result


@singledispatch
def run(arg) -> str:
    return ''


@run.register(RantBlockObject)
def _(block: RantBlockObject):
    attributes: BlockAttributes = BlockAttributeManager.get_attributes()
    block_result = ''
    while attributes.repetitions:
        attributes.repetitions = attributes.repetitions-1
        partial_result = interpret_internal(block.choices[randrange(0, len(block.choices))])
        block_result += partial_result
        if attributes.repetitions:
            block_result += attributes.separator
    return block_result


@run.register(RantFunctionObject)
def _(func: RantFunctionObject):
    if func.func in function_definitions:
        return function_definitions[func.func](func.args)


@run.register(RantTextObject)
def _(text: RantTextObject):
    return text.text
