import lexer.rant_lexer as Lexer
import parser.rant_parser as Parser
from .function_dict import function_definitions
from .block_attributes import BlockAttributeManager, BlockAttributes
from rant_exceptions import RantInterpreterException
from .synchronizer import Synchronizer, SynchronizerManager

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
    first_repetition = True
    synchronizer = None
    if attributes.synchronizer is not None:
        if SynchronizerManager.synchronizer_exists(attributes.synchronizer):
            synchronizer = SynchronizerManager.get_synchronizer(
                attributes.synchronizer)
        else:
            if attributes.synchronizer_type is None:
                raise RantInterpreterException(
                    f"[Interpreter.run](RantBlockObject) tried to define new synchronizer without defining synchronizer type")
            synchronizer = SynchronizerManager.create_synchronizer(attributes.synchronizer, attributes.synchronizer_type, len(block.choices))

    while attributes.repetitions:
        if synchronizer is None:
            choice = randrange(0,len(block.choices))
        else:
            choice = synchronizer.next()
        if first_repetition:
            first_repetition = False
            block_result += attributes.first
        elif attributes.repetitions == 1:
            block_result += attributes.last
        attributes.repetitions = attributes.repetitions-1
        partial_result = interpret_internal(
            block.choices[choice])
        block_result += partial_result
        if attributes.repetitions:
            block_result += attributes.separator
    return block_result


@run.register(RantFunctionObject)
def _(func: RantFunctionObject):
    if func.func in function_definitions:
        return function_definitions[func.func](func.args)
    else:
        raise RantInterpreterException(
            f"[Interpreter::run] no function found named '{func.func}'")


@run.register(RantTextObject)
def _(text: RantTextObject):
    return text.text
