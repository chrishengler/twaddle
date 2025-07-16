import os

from twaddle.exceptions import TwaddleDictionaryException
from twaddle.lookup.dictionary_file_parser import DictionaryFileParser
from twaddle.lookup.lookup_dictionary import LookupDictionary
from twaddle.compiler.compiler_objects import LookupObject


class LookupManager:
    def __init__(self):
        self.dictionaries = dict[str, LookupDictionary]()

    def __getitem__(self, name: str) -> LookupDictionary:
        return self.dictionaries[name]

    def add_dictionaries_from_folder(self, path: str):
        for f in os.listdir(path):
            if f.endswith(".dic"):
                dict_path = os.path.join(path, f)
                new_dictionary = DictionaryFileParser.read_from_file(dict_path)
                if new_dictionary is None:
                    raise TwaddleDictionaryException(
                        f"[LookupManager.add_dictionaries_from_folder] dictionary file {dict_path} could not be read."
                        "Are name and forms defined?"
                    )
                self.dictionaries[new_dictionary.name] = new_dictionary

    def clear_labels(self):
        for dictionary in self.dictionaries.values():
            dictionary.clear_labels()

    def do_lookup(self, lookup: LookupObject):
        dictionary: LookupDictionary = self.dictionaries[lookup.dictionary]
        return dictionary.get(lookup)
