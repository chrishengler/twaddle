from copy import copy
from functools import singledispatchmethod
from random import randint, randrange
from re import Match, sub
from typing import Optional

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
from twaddle.interpreter.function_definitions import boolean_helper
from twaddle.interpreter.function_dict import function_definitions
from twaddle.interpreter.regex_state import RegexState
from twaddle.interpreter.synchronizer import Synchronizer, SynchronizerManager
from twaddle.lookup.lookup_dictionary import LookupDictionary
from twaddle.lookup.lookup_manager import LookupManager
from twaddle.parser.transformer import TwaddleTransformer
from twaddle.parser.twaddle_parser import Lark_StandAlone as TwaddleParser
from twaddle.parser.twaddle_parser import (
    UnexpectedCharacters,
    UnexpectedInput,
    UnexpectedToken,
)

parser = TwaddleParser()
transformer = TwaddleTransformer()

TOKEN_NAMES = {
    "MORETHAN": "'>'",
    "LESSTHAN": "'<'",
    "LBRACE": "'{'",
    "RBRACE": "'}'",
    "LSQB": "'['",
    "RSQB": "']'",
    "PIPE": "'|'",
    "SEMICOLON": "';'",
    "DOT": "'.'",
    "MINUS": "'-'",
    "BACKSLASH": "'\\'",
    "FORWARD_SLASH": "'/'",
    "COLON": "':'",
    "TEXT": "text",
    "NAME": "identifier",
    "ESCAPED_CHAR": "escape character",
    "LABEL_MODIFIER": "'!' or '^'",
    "TAG_MODIFIER": "'!'",
}

# Examples for matching common parse errors to friendly messages
PARSE_ERROR_EXAMPLES = {
    "Unclosed block - missing '}'": [
        "{a|b",
        "{a|b|c",
    ],
    "Unclosed function - missing ']'": [
        "[rep:3",
        "[sync:name;locked",
    ],
    "Invalid function name: no whitespace allowed": [
        "[function name]",
    ],
    "Invalid lookup - unclosed or invalid whitespace in identifier": [
        "<noun",
        "<noun-tag",
        "<noun::=label",
        "<verb.past",
        "<noun::=a label>",
        "<noun-some tag>",
    ],
}


class Interpreter:
    SPECIAL_FUNCTIONS = ["clear", "load", "paste", "if"]

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
        self.saved_patterns = dict[str, BlockObject]()
        self.copied_blocks = dict[str, Formatter]()
        self.strict_mode = strict_mode

    def interpret_external(self, sentence: str) -> str:
        self.clear()
        try:
            tree = parser.parse(sentence)
            transformed_tree = transformer.transform(tree)
        except UnexpectedInput as err:
            raise TwaddleInterpreterException(self._format_parse_error(err, sentence))
        return self.interpret_internal(transformed_tree)

    def _format_parse_error(self, err: UnexpectedInput, sentence: str) -> str:
        context = err.get_context(sentence)

        # Try to match against known error patterns first
        label = err.match_examples(parser.parse, PARSE_ERROR_EXAMPLES)
        if label:
            return f"{label}\n{context}"

        # Fall back to generic message based on exception type
        if isinstance(err, UnexpectedToken):
            token = err.token
            if token.type == "$END":
                msg = "Unexpected end of input"
            else:
                msg = f"Unexpected '{token.value}'"
            expected = [e for e in err.expected if not e.startswith("_")]
            if expected:
                friendly = [TOKEN_NAMES.get(e, e) for e in expected]
                msg += f" (expected: {', '.join(friendly)})"
        elif isinstance(err, UnexpectedCharacters):
            msg = f"Unexpected character '{err.char}'"
            if err.allowed:
                friendly = [TOKEN_NAMES.get(e, e) for e in err.allowed]
                msg += f" (allowed: {', '.join(friendly)})"
        else:
            msg = "Parse error"
        return f"{msg}\n{context}\nSee the documentation at https://chrishengler.github.io/twaddle/ for help"

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
    def run(self, _arg: None) -> Formatter:
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
        if attributes.repetitions > 1 and attributes.while_predicate:
            raise TwaddleInterpreterException(
                "Cannot apply repeat and while to same block "
                "(try nesting [while] inside [repeat]-ed block if this was intentional)."
            )
        first_repetition = True
        if attributes.repetitions and (attributes.repetitions < 2):
            attributes.separator = None
            attributes.first = None
            attributes.last = None
        synchronizer = self._get_synchronizer_for_block(attributes, len(block.choices))

        def _continue():
            if attributes.while_predicate:
                attributes.while_iteration += 1
                if attributes.while_iteration > attributes.max_while_iterations:
                    return False
                return boolean_helper(self.run(attributes.while_predicate).resolve())
            if attributes.repetitions > 0:
                return True
            return False

        while _continue():
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
            formatter = Formatter.from_text("".join(reversed(block_result)))
        if attributes.abbreviate:
            abbreviation = self._get_abbreviation(formatter, attributes)
            formatter = Formatter.from_text(abbreviation)
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

    def _handle_special_functions(self, func: FunctionObject):
        match func.func:
            case "clear":
                self.force_clear()
                return Formatter()
            case "load":
                evaluated_args = [self.run(arg).resolve() for arg in func.args]
                return self._load_pattern(evaluated_args)
            case "paste":
                evaluated_args = [self.run(arg).resolve() for arg in func.args]
                return self._paste_block(evaluated_args)
            case "if":
                return self._handle_if(func)
            case _:
                raise TwaddleInterpreterException(
                    f"[Interpreter] function '{func.func}' "
                    "marked special but no special handling defined"
                )

    def _save_pattern(self, block: BlockObject, name: str):
        self.saved_patterns[name] = block

    def _load_pattern(self, evaluated_args: list[str]) -> Formatter:
        if not len(evaluated_args):
            raise TwaddleInterpreterException(
                "[Interpreter._handle_special_functions] Tried "
                "to load pattern without specifying name"
            )
        if not (block := self.saved_patterns.get(evaluated_args[0])):
            if len(evaluated_args) > 1:
                return Formatter.from_text(evaluated_args[1])
            raise TwaddleInterpreterException(
                "[Interpreter._handle_special_functions#load] Tried "
                f"to load unknown pattern '{evaluated_args[0]}'"
            )
        return self.run(block)

    def _paste_block(self, evaluated_args: list[str]) -> Formatter:
        if not len(evaluated_args):
            raise TwaddleInterpreterException(
                "[Interpreter._handle_special_functions] Tried "
                "to paste block result without specifying name"
            )
        if not (block := self.copied_blocks.get(evaluated_args[0])):
            if len(evaluated_args) > 1:
                return Formatter.from_text(evaluated_args[1])
            raise TwaddleInterpreterException(
                "[Interpreter._handle_special_functions#paste] Tried "
                f"to paste result of unknown block '{evaluated_args[0]}'"
            )
        return block

    def _handle_if(self, func: FunctionObject) -> Formatter:
        num_args = len(func.args)
        if num_args not in [2, 3]:
            raise TwaddleInterpreterException(
                f"[Interpreter._handle_if] if requires either two or three arguments, got {num_args}"
            )
        predicate_result = self.run(func.args[0]).resolve()
        predicate_bool = boolean_helper(predicate_result)
        if predicate_bool:
            return self.run(func.args[1])
        elif num_args == 3:
            return self.run(func.args[2])
        else:
            return Formatter()

    @run.register(FunctionObject)
    def _(self, func: FunctionObject):
        formatter = Formatter()
        if func.func in self.SPECIAL_FUNCTIONS:
            return self._handle_special_functions(func)
        evaluated_args = [self.run(arg).resolve() for arg in func.args]
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
        return Formatter.from_text(text.text)

    @run.register(LookupObject)
    def _(self, lookup: LookupObject):
        formatter = Formatter()
        dictionary: LookupDictionary = self.lookup_manager[lookup.dictionary]
        formatter.append(dictionary.get(lookup, self.strict_mode))
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
        return Formatter.from_text(str(randint(0, 9)))

    @run.register(RegexObject)
    def _(self, regex: RegexObject):
        # noinspection SpellCheckingInspection

        def repl(matchobj: Match[str]):
            RegexState.match = matchobj.group()
            return self.run(regex.replacement).resolve()

        return Formatter.from_text(
            sub(regex.regex, repl, self.run(regex.scope).resolve())
        )
