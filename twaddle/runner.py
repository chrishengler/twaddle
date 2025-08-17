from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


class TwaddleRunner:
    def __init__(
        self,
        path: str,
        persistent: bool = False,
        persistent_labels: bool = False,
        persistent_synchronizers: bool = False,
    ):
        self.lookup_manager = LookupManager()
        self.lookup_manager.add_dictionaries_from_folder(path)
        persistent_labels = True if persistent else persistent_labels
        persistent_synchronizers = True if persistent else persistent_synchronizers
        self.interpreter = Interpreter(
            self.lookup_manager,
            persistent_labels=persistent_labels,
            persistent_synchronizers=persistent_synchronizers,
        )
        pass

    def run_sentence(self, sentence: str) -> str:
        return self.interpreter.interpret_external(sentence)

    def clear(self) -> None:
        self.interpreter.force_clear()
