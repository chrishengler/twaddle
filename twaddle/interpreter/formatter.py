import re
from typing import Type

from twaddle.exceptions import TwaddleInterpreterException
from twaddle.parser.compiler_objects import IndefiniteArticleObject

from .formatting_object import (
    FormattingObject,
    FormattingStrategy,
    IndefiniteArticle,
    PlainText,
    StrategyChange,
)


class Formatter:
    # regex for finding next alphabetic string
    alphabetic_regex = re.compile(r"[^\W_]+", re.UNICODE)

    def __init__(self):
        self.output_stack = list()
        self.sentence = str()
        self.current_strategy = FormattingStrategy.NONE
        self.indefinite_article_waiting = False

    def _reset_(self):
        self.output_stack = list()
        self.sentence = str()
        self.current_strategy = FormattingStrategy.NONE
        self.indefinite_article_waiting = False

    def append(
        self,
        item: str | FormattingStrategy | IndefiniteArticleObject | FormattingObject,
    ):
        if item is None:
            return
        elif isinstance(item, FormattingStrategy):
            self.output_stack.append(StrategyChange(self._get_previous_object_(), item))
            return
        elif isinstance(item, str):
            previous = self._get_previous_object_()
            self.output_stack.append(PlainText(previous, item))
            if self.indefinite_article_waiting:
                self._replace_indefinite_articles(item)
            return
        elif isinstance(item, IndefiniteArticleObject):
            self.add_indefinite_article(item.default_upper)
        elif isinstance(item, IndefiniteArticle):
            self.add_indefinite_article(item.default_upper)
        elif isinstance(item, PlainText):
            previous = self._get_previous_object_()
            self.output_stack.append(PlainText(previous, item.text))
            if self.indefinite_article_waiting:
                self._replace_indefinite_articles(item.text)
        elif isinstance(item, FormattingObject):
            item.previous = self._get_previous_object_()
            self.output_stack.append(item)
        else:
            raise TwaddleInterpreterException(
                f"[Formatter.append] tried to append unexpected type {type(item)}"
            )

    def _get_previous_object_(self) -> Type[FormattingObject] | None:
        if len(self.output_stack):
            return self.output_stack[-1]
        return None

    def _print_(self, text_object: PlainText):
        self._append_to_sentence_(text_object.text)

    def _default_indefinite_article_(self, _: IndefiniteArticle):
        self._append_to_sentence_("a")

    def _append_to_sentence_(self, text: str):
        match self.current_strategy:
            case FormattingStrategy.NONE:
                self.sentence += text
            case FormattingStrategy.UPPER:
                self.sentence += text.upper()
            case FormattingStrategy.LOWER:
                self.sentence += text.lower()
            case FormattingStrategy.SENTENCE:
                self.sentence += self.apply_sentence_case(text)
            case FormattingStrategy.TITLE:
                self.sentence += self.apply_title_case(text)
            case _:
                raise TwaddleInterpreterException(
                    f"[Formatter.append] no handling defined for {self.current_strategy}"
                )

    def __iadd__(self, other):
        for item in other.output_stack:
            self.append(item)
        return self

    def resolve(self) -> str:
        function_dict = {
            PlainText: self._print_,
            StrategyChange: self._set_strategy_,
            IndefiniteArticle: self._default_indefinite_article_,
        }
        for item in self.output_stack:
            function_dict[type(item)](item)
        result = self.sentence
        self._reset_()
        return result

    def set_strategy(self, strategy: FormattingStrategy):
        self.output_stack.append(StrategyChange(self._get_previous_object_(), strategy))

    def _set_strategy_(self, strategy: StrategyChange):
        self.current_strategy = strategy.strategy

    def add_indefinite_article(self, default_upper=False):
        previous = self._get_previous_object_()
        self.output_stack.append(IndefiniteArticle(previous, default_upper))
        self.indefinite_article_waiting = True

    def _replace_indefinite_articles(self, text: str):
        next_word = self._find_alphabetic_string_(text)
        if next_word is None:
            return
        chosen_article = "an" if self._indefinite_article_use_an_(next_word) else "a"
        self.output_stack = [
            item
            if not isinstance(item, IndefiniteArticle)
            else self._convert_article(item, chosen_article)
            for item in self.output_stack
        ]

    def _convert_article(
        self, article: IndefiniteArticle, chosen_article: str
    ) -> PlainText:
        if article.default_upper:
            chosen_article = chosen_article.capitalize()
        self.indefinite_article_waiting = False
        result = PlainText(article.previous, chosen_article)
        if article.next:
            result.next = article.next
            article.next.previous = result
        return PlainText(article.previous, chosen_article)

    def _find_alphabetic_string_(self, text: str) -> str | None:
        result = self.alphabetic_regex.search(text)
        if result:
            return result[0]
        return None

    # noinspection SpellCheckingInspection
    def _indefinite_article_use_an_(self, next_word: str) -> bool:
        # exclude/include prefixes/words taken directly from old version of rant
        # this can definitely be improved but will do for now
        irregular_a_prefixes = {
            "uni",
            "use",
            "uri",
            "urol",
            "U.",
            "one",
            "uvu",
            "eul",
            "euk",
            "eur",
        }
        irregular_an_prefixes = {"honest", "honor", "hour", "8"}
        irregular_a_words = {"u"}
        irregular_an_words = {"f", "fbi", "fcc", "fda", "x", "l", "m", "n", "s", "h"}
        if any(next_word.startswith(prefix) for prefix in irregular_a_prefixes):
            return False
        if any(next_word == word for word in irregular_a_words):
            return False
        if any(next_word.startswith(prefix) for prefix in irregular_an_prefixes):
            return True
        if any(next_word == word for word in irregular_an_words):
            return True
        return next_word[0].lower() in ["a", "e", "i", "o", "u"]

    def apply_sentence_case(self, text: str) -> str:
        result = str()
        sentence_start = False
        if not self.sentence or self.sentence.rstrip()[-1] in ".!?":
            sentence_start = True
        for char in text:
            if sentence_start:
                result += char.upper()
            else:
                result += char.lower()
            if not char.isspace():
                sentence_start = char in ".!?"
        return result

    def apply_title_case(self, text: str) -> str:
        result = str()
        word_start = False
        if not self.sentence or self.sentence[-1].isspace():
            word_start = True
        for char in text:
            if word_start:
                result += char.upper()
            else:
                result += char.lower()
            word_start = True if char.isspace() else False
        return result
