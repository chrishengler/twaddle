import lexer.rant_lexer as Lexer
from parser.rant_compiler import RantCompiler
from .function_dict import function_definitions
from .block_attributes import BlockAttributeManager, BlockAttributes
from rant_exceptions import RantInterpreterException
from .synchronizer import Synchronizer, SynchronizerManager
import interpreter.formatter as Formatter
from lookup.lookup import LookupManager

from collections import deque
from functools import singledispatch
from parser.rant_object import *
from random import randrange


compiler = RantCompiler()

def interpret_external(sentence: str) -> str:
    SynchronizerManager.clear()
    BlockAttributeManager.clear()
    LookupManager.clear_labels()
    return interpret_internal(compiler.compile(sentence))


def interpret_internal(parse_result: deque[RantObject]) -> str:
    result: str = ""

    for obj in parse_result:
        obj_result = run(obj)
        if obj_result is not None:
            Formatter.append(obj_result)
    return Formatter.get()


@singledispatch
def run(arg) -> str:
    return ''

@run.register(RantRootObject)
def _(block: RantRootObject):
    result = ''
    for item in block.contents:
        result += run(item)
    return result

@run.register(RantBlockObject)
def _(block: RantBlockObject):
    attributes: BlockAttributes = BlockAttributeManager.get_attributes()
    block_result = ''
    first_repetition = True
    synchronizer: Synchronizer = None
    if attributes.synchronizer is not None:
        if SynchronizerManager.synchronizer_exists(attributes.synchronizer):
            synchronizer = SynchronizerManager.get_synchronizer(
                attributes.synchronizer)
        else:
            if attributes.synchronizer_type is None:
                raise RantInterpreterException(
                    f"[Interpreter.run](RantBlockObject) tried to define new synchronizer without defining synchronizer type")
            synchronizer = SynchronizerManager.create_synchronizer(
                attributes.synchronizer, attributes.synchronizer_type, len(block.choices))

    while attributes.repetitions:
        if synchronizer is None:
            choice = randrange(0, len(block.choices))
        else:
            choice = synchronizer.next()
            if choice >= len(block.choices):
                raise RantInterpreterException(
                    f"[Interpreter.run](RantBlockObject) tried to get item no. {choice} of {len(block.choices)} - when using synchronizers, make sure you have the same number of choices each time")
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
    evaluated_args = list()
    for arg in func.args:
        evaluated_args.append(run(arg))
    if func.func in function_definitions:
        return function_definitions[func.func](evaluated_args)
    else:
        raise RantInterpreterException(
            f"[Interpreter::run] no function found named '{func.func}'")


@run.register(RantTextObject)
def _(text: RantTextObject):
    return text.text

@run.register(RantLookupObject)
def _(lookup: RantLookupObject):
    dictionary = LookupManager[lookup.dictionary]
    return dictionary.get(lookup)

@run.register(RantIndefiniteArticleObject)
def _(indef: RantIndefiniteArticleObject):
    Formatter.add_indefinite_article(indef.default_upper)
    return None

