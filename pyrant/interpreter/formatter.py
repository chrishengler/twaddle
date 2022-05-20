from rant_exceptions import RantInterpreterException
from .formatting_object import *

output_stack = list()
sentence = str()
current_strategy = FormattingStrategy.NONE


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
        previous = _get_previous_object()
        output_stack.append(PlainText(previous, text))


def _get_previous_object() -> type[FormattingObject]:
    if len(output_stack):
        return output_stack[-1]
    return None


def _print_(text_object: PlainText):
    global sentence
    text = text_object.text
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
    output_stack.append(StrategyChange(_get_previous_object(), strategy))


def _set_strategy_(strategy: FormattingStrategy):
    global current_strategy
    current_strategy = strategy.strategy


def _apply_indefinite_article_(article: IndefiniteArticle):
    global sentence


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
