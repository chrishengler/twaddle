from lookup.lookup import LookupManager
from interpreter.interpreter import interpret_external as interpret


class Rant:
    def __init__(self, path: str):
        LookupManager.add_dictionaries_from_folder(path)
        pass

    def run_sentence(self, sentence: str) -> str:
        return interpret(sentence)
