from functools import singledispatchmethod
from random import randint, randrange
from re import Match, sub

from twaddle.compiler.compiler import Compiler
from twaddle.compiler.compiler_objects import (
    BlockObject,
    DigitObject,
    FunctionObject,
    IndefiniteArticleObject,
    LookupObject,
    RegexObject,
    RootObject,
    TextObject,
)
from twaddle.exceptions import TwaddleInterpreterException
from twaddle.interpreter.block_attributes import BlockAttributeManager, BlockAttributes
from twaddle.interpreter.formatter import Formatter
from twaddle.interpreter.function_dict import function_definitions
from twaddle.interpreter.regex_state import RegexState
from twaddle.interpreter.synchronizer import Synchronizer, SynchronizerManager
from twaddle.lookup.lookup_dictionary import LookupDictionary
from twaddle.lookup.lookup_manager import LookupManager


class Interpreter:
    def __init__(
        self,
        lookup_manager: LookupManager,
        persistent_labels: bool = False,
        persistent_synchronizers: bool = False,
    ):
        self.persistent_labels = persistent_labels
        self.persistent_synchronizers = persistent_synchronizers
        self.lookup_manager = lookup_manager
        self.synchronizer_manager = SynchronizerManager()
        self.block_attribute_manager = BlockAttributeManager()
        self.compiler = Compiler()

    def interpret_external(self, sentence: str) -> str:
        self.clear()
        compiled_sentence = self.compiler.compile(sentence)
        return self.interpret_internal(compiled_sentence)

    def interpret_internal(self, parse_result: RootObject) -> str:
        formatter = Formatter()
        for obj in parse_result:
            resulting_formatter = self.run(obj)
            if resulting_formatter:
                formatter += resulting_formatter
        result = formatter.resolve()
        return result

    def clear(self):
        if not self.persistent_labels:
            self.lookup_manager.clear_labels()
        if not self.persistent_synchronizers:
            self.synchronizer_manager.clear()
        self.block_attribute_manager.clear()

    def force_clear(self):
        self.lookup_manager.clear_labels()
        self.synchronizer_manager.clear()
        self.block_attribute_manager.clear()

    # noinspection PyUnusedLocal
    @singledispatchmethod
    def run(self, arg) -> Formatter:
        formatter = Formatter()
        return formatter

    @run.register(RootObject)
    def _(self, root: RootObject):
        formatter = Formatter()
        for item in root.contents:
            item_result = self.run(item)
            if item_result:
                formatter += item_result
        return formatter

    @run.register(BlockObject)
    def _(self, block: BlockObject):
        formatter = Formatter()
        attributes: BlockAttributes = self.block_attribute_manager.get_attributes()
        first_repetition = True
        if attributes.repetitions < 2:
            attributes.separator = None
            attributes.first = None
            attributes.last = None
        synchronizer: Synchronizer | None = None
        if attributes.synchronizer is not None:
            if self.synchronizer_manager.synchronizer_exists(attributes.synchronizer):
                synchronizer = self.synchronizer_manager.get_synchronizer(
                    attributes.synchronizer
                )
            else:
                if attributes.synchronizer_type is None:
                    raise TwaddleInterpreterException(
                        "[Interpreter.run](RantBlockObject) tried to define new synchronizer "
                        "without defining synchronizer type"
                    )
                synchronizer = self.synchronizer_manager.create_synchronizer(
                    attributes.synchronizer,
                    attributes.synchronizer_type,
                    len(block.choices),
                )

        while attributes.repetitions:
            if synchronizer is None:
                choice = randrange(0, len(block.choices))
            else:
                choice = synchronizer.next()
                if choice >= len(block.choices):
                    raise TwaddleInterpreterException(
                        f"[Interpreter.run](RantBlockObject) tried to get item no. {choice} of {len(block.choices)} -"
                        "when using synchronizers, make sure you have the same number of choices each time"
                    )
            if first_repetition and attributes.first:
                first_repetition = False
                formatter.append_formatter(self.run(attributes.first))
            elif attributes.repetitions == 1:
                if attributes.last:
                    formatter.append_formatter(self.run(attributes.last))
                elif attributes.separator:
                    formatter.append_formatter(self.run(attributes.separator))
            attributes.repetitions = attributes.repetitions - 1
            partial_result = self.run(block.choices[choice])
            formatter += partial_result
            if attributes.repetitions > 1 and attributes.separator:
                formatter.append_formatter(self.run(attributes.separator))
            if attributes.hidden:
                return Formatter()
        return formatter

    @run.register(FunctionObject)
    def _(self, func: FunctionObject):
        formatter = Formatter()
        evaluated_args = list()
        for arg in func.args:
            evaluated_args.append(self.run(arg).resolve())
        if func.func == "clear":  # special case
            self.force_clear()
            return formatter
        if func.func in function_definitions:
            formatter.append(
                function_definitions[func.func](
                    evaluated_args, self.block_attribute_manager, func.args
                )
            )
        else:
            raise TwaddleInterpreterException(
                f"[Interpreter::run] no function found named '{func.func}'"
            )
        return formatter

    @run.register(TextObject)
    def _(self, text: TextObject):
        formatter = Formatter()
        formatter.append(text.text)
        return formatter

    @run.register(LookupObject)
    def _(self, lookup: LookupObject):
        formatter = Formatter()
        dictionary: LookupDictionary = self.lookup_manager[lookup.dictionary]
        formatter.append(dictionary.get(lookup))
        return formatter

    # noinspection SpellCheckingInspection
    @run.register(IndefiniteArticleObject)
    def _(self, indef: IndefiniteArticleObject):
        formatter = Formatter()
        formatter.add_indefinite_article(indef.default_upper)
        return formatter

    # noinspection PyUnusedLocal
    @run.register(DigitObject)
    def _(self, digit: DigitObject):
        formatter = Formatter()
        formatter.append(str(randint(0, 9)))
        return formatter

    @run.register(RegexObject)
    def _(self, regex: RegexObject):
        # noinspection SpellCheckingInspection
        formatter = Formatter()

        def repl(matchobj: Match):
            RegexState.match = matchobj.group()
            return self.run(regex.replacement).resolve()

        formatter.append(sub(regex.regex, repl, self.run(regex.scope).resolve()))
        return formatter
