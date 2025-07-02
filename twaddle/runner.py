from twaddle.interpreter.interpreter import interpret_external as interpret
from twaddle.lookup.lookup import LookupManager


class TwaddleRunner:
    def __init__(self, path: str):
        LookupManager.add_dictionaries_from_folder(path)
        pass

    @staticmethod
    def run_sentence(sentence: str) -> str:
        return interpret(sentence)
