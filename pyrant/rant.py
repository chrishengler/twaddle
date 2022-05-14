from lookup.lookup import LookupDictionaryManager
from interpreter.interpreter import interpret_external as interpret

class Rant:
    def __init__(self, path: str):
        LookupDictionaryManager.add_dictionaries_from_folder(path)

    def run_sentence(self, sentence: str) -> str:
        return interpret(sentence)

