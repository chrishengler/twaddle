from importlib.resources import as_file
from importlib.resources.abc import Traversable
from pathlib import Path

from twaddle.interpreter.interpreter import Interpreter
from twaddle.lookup.lookup_manager import LookupManager


class TwaddleRunner:
    def __init__(
        self,
        path: str | Path | Traversable,
        persistent: bool = False,
        persistent_labels: bool = False,
        persistent_synchronizers: bool = False,
        persistent_patterns: bool = False,
        persistent_clipboard: bool = False,
        strict_mode: bool = False,
    ):
        # Handle Traversable objects from importlib.resources
        if isinstance(path, Traversable):
            with as_file(path) as directory:
                self._initialize(
                    directory,
                    persistent,
                    persistent_labels,
                    persistent_synchronizers,
                    persistent_patterns,
                    persistent_clipboard,
                    strict_mode,
                )
        else:
            if not isinstance(path, Path):
                path = Path(path)
            self._initialize(
                path,
                persistent,
                persistent_labels,
                persistent_synchronizers,
                persistent_patterns,
                persistent_clipboard,
                strict_mode,
            )

    def _initialize(
        self,
        path: Path,
        persistent: bool,
        persistent_labels: bool,
        persistent_synchronizers: bool,
        persistent_patterns: bool,
        persistent_clipboard: bool,
        strict_mode: bool,
    ):
        self.lookup_manager = LookupManager()
        self.lookup_manager.add_dictionaries_from_folder(path)
        persistent_labels = True if persistent else persistent_labels
        persistent_synchronizers = True if persistent else persistent_synchronizers
        persistent_patterns = True if persistent else persistent_patterns
        persistent_clipboard = True if persistent else persistent_clipboard
        self.interpreter = Interpreter(
            self.lookup_manager,
            persistent_labels=persistent_labels,
            persistent_synchronizers=persistent_synchronizers,
            persistent_patterns=persistent_patterns,
            persistent_clipboard=persistent_clipboard,
            strict_mode=strict_mode,
        )

    def add_dictionaries_from_folder(self, path: str | Path | Traversable):
        if isinstance(path, Traversable):
            with as_file(path) as directory:
                self.lookup_manager.add_dictionaries_from_folder(directory)
        else:
            if not isinstance(path, Path):
                path = Path(path)
            self.lookup_manager.add_dictionaries_from_folder(path)

    def add_dictionary_file(self, path: str | Path | Traversable):
        if isinstance(path, Traversable):
            with as_file(path) as file:
                self.lookup_manager.add_dictionary_file(file)
        else:
            if not isinstance(path, Path):
                path = Path(path)
            self.lookup_manager.add_dictionary_file(path)

    def run_sentence(self, sentence: str) -> str:
        return self.interpreter.interpret_external(sentence)

    def clear(self) -> None:
        self.interpreter.force_clear()
