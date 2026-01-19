from pathlib import Path

from twaddle.compiler.compiler_objects import LookupObject
from twaddle.exceptions import TwaddleDictionaryException
from twaddle.lookup.dictionary_file_parser import DictionaryFileParser
from twaddle.lookup.lookup_dictionary import LookupDictionary


class LookupManager:
    def __init__(self):
        self.dictionaries = dict[str, LookupDictionary]()

    def __getitem__(self, name: str) -> LookupDictionary:
        if dictionary := self.dictionaries.get(name):
            return dictionary
        raise TwaddleDictionaryException(
            f"[LookupManager.__getitem__] No dictionary loaded named {name}"
        )

    def add_dictionaries_from_folder(self, path: Path):
        if isinstance(path, str):
            path = Path(path)
        for entry in path.iterdir():
            if entry.name.endswith(".dic") and entry.is_file():
                self.add_dictionary_file(entry)

    def add_dictionary_file(self, path: Path):
        new_dictionary = DictionaryFileParser.read_from_path(path)
        if new_dictionary is None:
            exception = TwaddleDictionaryException(
                f"[LookupManager.add_dictionaries_from_folder] dictionary file {path} could not be read. "
                "Are name and forms defined?"
            )
            print(f"{str(exception)=}")
            raise exception
        self.dictionaries[new_dictionary.name] = new_dictionary

    def clear_labels(self):
        for dictionary in self.dictionaries.values():
            dictionary.clear_labels()

    def do_lookup(self, lookup: LookupObject):
        dictionary: LookupDictionary = self.dictionaries[lookup.dictionary]
        return dictionary.get(lookup)
