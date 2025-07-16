from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


class TwaddleRunner:
    def __init__(self, path: str):
        self.lookup_manager = LookupManager()
        self.lookup_manager.add_dictionaries_from_folder(path)
        self.interpreter = Interpreter(self.lookup_manager)
        pass

    def run_sentence(self, sentence: str) -> str:
        return self.interpreter.interpret_external(sentence)
