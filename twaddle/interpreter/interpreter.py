from copy import copy
from functools import singledispatchmethod
from random import randint, randrange
from re import Match, sub
from typing import Optional

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
    SPECIAL_FUNCTIONS = ["clear", "load", "paste"]

    def __init__(
        self,
        lookup_manager: LookupManager,
        persistent_labels: bool = False,
        persistent_synchronizers: bool = False,
        persistent_patterns: bool = False,
        persistent_clipboard: bool = False,
        strict_mode: bool = False,
    ):
        self.persistent_labels = persistent_labels
        self.persistent_synchronizers = persistent_synchronizers
        self.persistent_patterns = persistent_patterns
        self.persistent_clipboard = persistent_clipboard
        self.lookup_manager = lookup_manager
        self.synchronizer_manager = SynchronizerManager()
        self.block_attribute_manager = BlockAttributeManager()
        self.compiler = Compiler(strict_mode=strict_mode)
        self.saved_patterns = dict()
        self.copied_blocks = dict()
        self.strict_mode = strict_mode

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
        if not self.persistent_patterns:
            self.saved_patterns.clear()
        if not self.persistent_clipboard:
            self.copied_blocks.clear()
        self.block_attribute_manager.clear()

    def force_clear(self):
        self.lookup_manager.clear_labels()
        self.synchronizer_manager.clear()
        self.saved_patterns.clear()
        self.block_attribute_manager.clear()
        self.copied_blocks.clear()

    def _get_synchronizer_for_block(
        self, attributes: BlockAttributes, num_choices: int
    ) -> Optional[Synchronizer]:
        if attributes.synchronizer is None:
            return None
        if self.synchronizer_manager.synchronizer_exists(attributes.synchronizer):
            synchronizer = self.synchronizer_manager.get_synchronizer(
                attributes.synchronizer
            )
            if self.strict_mode and synchronizer.num_choices != num_choices:
                raise TwaddleInterpreterException(
                    f"[Interpreter._get_synchronizer_for_block] Invalid number of choices ({num_choices}) "
                    f"for synchronizer '{attributes.synchronizer}', initialised with {synchronizer.num_choices}"
                )
            return synchronizer
        if attributes.synchronizer_type is None:
            raise TwaddleInterpreterException(
                "[Interpreter.run](RantBlockObject) tried to define new synchronizer "
                "without defining synchronizer type"
            )
        return self.synchronizer_manager.create_synchronizer(
            attributes.synchronizer,
            attributes.synchronizer_type,
            num_choices,
        )

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
        synchronizer = self._get_synchronizer_for_block(attributes, len(block.choices))

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
        if name := attributes.save_as:
            self.saved_patterns[name] = block
        if name := attributes.copy_as:
            self.copied_blocks[name] = copy(formatter)
        if attributes.hidden:
            return Formatter()
        if attributes.reverse:
            block_result = formatter.resolve()
            formatter = Formatter()
            formatter.append("".join(reversed(block_result)))
        if attributes.abbreviate:
            abbreviation = self._get_abbreviation(formatter, attributes)
            formatter = Formatter()
            formatter.append(abbreviation)
        return formatter

    def _get_abbreviation(
        self, input_formatter: Formatter, attributes: BlockAttributes
    ) -> str:
        output_formatter = Formatter()
        if case := attributes.abbreviation_case:
            output_formatter.set_strategy(case)

        def _get_abbr_component(word: str) -> str:
            for index, char in enumerate(word):
                if char.isalpha():
                    return char
                if char.isdigit():
                    digits = ""
                    while char.isdigit():
                        digits += str(char)
                        index += 1
                        if index >= len(word):
                            break
                        char = word[index]
                    return digits
            return ""

        abbreviation = "".join(
            [_get_abbr_component(word) for word in input_formatter.resolve().split()]
        )
        output_formatter.append(abbreviation)
        return output_formatter.resolve()

    def _handle_special_functions(
        self, func: FunctionObject, evaluated_args: list[str]
    ):
        match func.func:
            case "clear":
                self.force_clear()
                return Formatter()
            case "load":
                if not len(evaluated_args):
                    raise TwaddleInterpreterException(
                        "[Interpreter._handle_special_functions] Tried "
                        "to load pattern without specifying name"
                    )
                if not (block := self.saved_patterns.get(evaluated_args[0])):
                    raise TwaddleInterpreterException(
                        "[Interpreter._handle_special_functions#load] Tried "
                        f"to load unknown pattern '{evaluated_args[0]}'"
                    )
                return self.run(block)
            case "paste":
                if not len(evaluated_args):
                    raise TwaddleInterpreterException(
                        "[Interpreter._handle_special_functions] Tried "
                        "to paste block result without specifying name"
                    )
                if not (block := self.copied_blocks.get(evaluated_args[0])):
                    raise TwaddleInterpreterException(
                        "[Interpreter._handle_special_functions#paste] Tried "
                        f"to paste result of unknown block '{evaluated_args[0]}'"
                    )
                return block
            case _:
                raise TwaddleInterpreterException(
                    f"[Interpreter] function '{func.func}' "
                    "marked special but no special handling defined"
                )

    def _save_pattern(self, block: BlockObject, name: str):
        self.saved_patterns[name] = block

    @run.register(FunctionObject)
    def _(self, func: FunctionObject):
        formatter = Formatter()
        evaluated_args = list()
        for arg in func.args:
            evaluated_args.append(self.run(arg).resolve())
        if func.func in self.SPECIAL_FUNCTIONS:
            return self._handle_special_functions(func, evaluated_args)
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
