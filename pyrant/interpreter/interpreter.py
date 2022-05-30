from parser.compiler import Compiler
from .function_dict import function_definitions
from .block_attributes import BlockAttributeManager, BlockAttributes
from rant_exceptions import RantInterpreterException
from .synchronizer import Synchronizer, SynchronizerManager
import interpreter.formatter as formatter
from lookup.lookup import LookupManager, LookupDictionary
from parser.compiler_objects import *
from .regex_state import RegexState

from functools import singledispatch
from random import randrange, randint
from re import sub, Match

compiler = Compiler()


def interpret_external(sentence: str) -> str:
    SynchronizerManager.clear()
    BlockAttributeManager.clear()
    LookupManager.clear_labels()
    return interpret_internal(compiler.compile(sentence))


def interpret_internal(parse_result: RootObject) -> str:
    for obj in parse_result:
        obj_result = run(obj)
        if obj_result is not None:
            formatter.append(obj_result)
    return formatter.get()


# noinspection PyUnusedLocal
@singledispatch
def run(arg) -> str:
    return ''


@run.register(RootObject)
def _(block: RootObject):
    result = ''
    for item in block.contents:
        item_result = run(item)
        if item_result:
            result += item_result
    return result


@run.register(BlockObject)
def _(block: BlockObject):
    attributes: BlockAttributes = BlockAttributeManager.get_attributes()
    block_result = ''
    first_repetition = True
    synchronizer: Synchronizer | None = None
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
        attributes.repetitions = attributes.repetitions - 1
        partial_result = interpret_internal(
            block.choices[choice])
        block_result += partial_result
        if attributes.repetitions:
            block_result += attributes.separator
    return block_result


@run.register(FunctionObject)
def _(func: FunctionObject):
    evaluated_args = list()
    for arg in func.args:
        evaluated_args.append(run(arg))
    if func.func in function_definitions:
        return function_definitions[func.func](evaluated_args)
    else:
        raise RantInterpreterException(
            f"[Interpreter::run] no function found named '{func.func}'")


@run.register(TextObject)
def _(text: TextObject):
    return text.text


@run.register(LookupObject)
def _(lookup: LookupObject):
    dictionary: LookupDictionary = LookupManager[lookup.dictionary]
    return dictionary.get(lookup)


# noinspection SpellCheckingInspection
@run.register(IndefiniteArticleObject)
def _(indef: IndefiniteArticleObject):
    formatter.add_indefinite_article(indef.default_upper)
    return None


# noinspection PyUnusedLocal
@run.register(DigitObject)
def _(digit: DigitObject):
    return str(randint(0, 9))


@run.register(RegexObject)
def _(regex: RegexObject):
    # noinspection SpellCheckingInspection
    def repl(matchobj: Match):
        RegexState.match = matchobj.group()
        return run(regex.replacement)

    return sub(regex.regex, repl, run(regex.scope))
