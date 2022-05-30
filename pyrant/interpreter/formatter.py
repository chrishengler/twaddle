from rant_exceptions import RantInterpreterException
from .formatting_object import *
import re

output_stack = list()
sentence = str()
current_strategy = FormattingStrategy.NONE

# regex for finding next alphabetic string
alphabetic_regex = re.compile(r"[^\W_]+", re.UNICODE)


def reset():
    global output_stack, sentence, current_strategy
    output_stack = list()
    sentence = str()
    current_strategy = FormattingStrategy.NONE


def append(text: str):
    global output_stack
    if text is None:
        return
    else:
        previous = _get_previous_object_()
        output_stack.append(PlainText(previous, text))


def _get_previous_object_() -> Type[FormattingObject] | None:
    if len(output_stack):
        return output_stack[-1]
    return None


def _print_(text_object: PlainText):
    _append_to_sentence_(text_object.text)


def _append_to_sentence_(text: str):
    global sentence
    match current_strategy:
        case FormattingStrategy.NONE:
            sentence += text
        case FormattingStrategy.UPPER:
            sentence += text.upper()
        case FormattingStrategy.LOWER:
            sentence += text.lower()
        case FormattingStrategy.SENTENCE:
            sentence += apply_sentence_case(text)
        case FormattingStrategy.TITLE:
            sentence += apply_title_case(text)
        case _:
            raise RantInterpreterException(
                f"[Formatter.append] no handling defined for {current_strategy}")


def get() -> str:
    function_dict = {PlainText: _print_,
                     StrategyChange: _set_strategy_,
                     IndefiniteArticle: _apply_indefinite_article_,
                     }
    for item in output_stack:
        function_dict[type(item)](item)
    result = sentence
    reset()
    return result


def set_strategy(strategy: FormattingStrategy):
    global output_stack
    output_stack.append(StrategyChange(_get_previous_object_(), strategy))


def _set_strategy_(strategy: StrategyChange):
    global current_strategy
    current_strategy = strategy.strategy


def add_indefinite_article(default_upper=False):
    global output_stack
    previous = _get_previous_object_()
    output_stack.append(IndefiniteArticle(previous, default_upper))


def _apply_indefinite_article_(article: IndefiniteArticle):
    global sentence
    next_word = _next_alphanumeric_string_(article)
    chosen_article = 'an' if _indefinite_article_use_an_(next_word) else 'a'
    if article.default_upper:
        chosen_article = chosen_article.capitalize()
    _append_to_sentence_(chosen_article)


def _next_alphanumeric_string_(item: Type[FormattingObject]) -> str | None:
    if isinstance(item, PlainText):
        result = alphabetic_regex.search(item.text)
        if result:
            return result[0]
    if item.next:
        return _next_alphanumeric_string_(item.next)
    return None


# noinspection SpellCheckingInspection
def _indefinite_article_use_an_(next_word: str) -> bool:
    # exclude/include prefixes/words taken directly from old version of rant
    # this can definitely be improved but will do for now
    irregular_a_prefixes = {"uni", "use", "uri",
                            "urol", "U.", "one", "uvu", "eul", "euk", "eur"}
    irregular_an_prefixes = {"honest", "honor", "hour", "8"}
    irregular_a_words = {"u"}
    irregular_an_words = {"f", "fbi", "fcc",
                          "fda", "x", "l", "m", "n", "s", "h"}
    if any(next_word.startswith(prefix) for prefix in irregular_a_prefixes):
        return False
    if any(next_word == word for word in irregular_a_words):
        return False
    if any(next_word.startswith(prefix) for prefix in irregular_an_prefixes):
        return True
    if any(next_word == word for word in irregular_an_words):
        return True
    return next_word[0].lower() in ['a', 'e', 'i', 'o', 'u']


def apply_sentence_case(text: str) -> str:
    result = str()
    sentence_start = False
    if not sentence or sentence.rstrip()[-1] in ".!?":
        sentence_start = True
    for char in text:
        if sentence_start:
            result += char.upper()
        else:
            result += char.lower()
        if not char.isspace():
            sentence_start = char in ".!?"
    return result


def apply_title_case(text: str) -> str:
    result = str()
    word_start = False
    if not sentence or sentence[-1].isspace():
        word_start = True
    for char in text:
        if word_start:
            result += char.upper()
        else:
            result += char.lower()
        word_start = True if char.isspace() else False
    return result
