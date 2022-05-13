from rant_exceptions import RantInterpreterException
from .formatting_strategy import FormattingStrategy

sentence = str()
current_strategy = FormattingStrategy.NONE

def reset():
    global sentence, current_strategy
    sentence = str()
    current_strategy = FormattingStrategy.NONE


def append(text: str):
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
                f"[Formatter.append] no handling defined for {strategy}")

def get() -> str:
    result = sentence
    reset()
    return result


def set_strategy(strategy: FormattingStrategy):
    global current_strategy
    current_strategy = strategy

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
