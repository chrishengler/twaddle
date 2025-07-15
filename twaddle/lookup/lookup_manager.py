from twaddle.exceptions import TwaddleDictionaryException
from twaddle.lookup.lookup_dictionary_factory import LookupDictionaryFactory
from twaddle.lookup.lookup_dictionary import LookupDictionary
from twaddle.parser.compiler_objects import LookupObject


import os


class LookupManager:
    factory = LookupDictionaryFactory()
    dictionaries = dict[str, LookupDictionary]()

    @staticmethod
    def __class_getitem__(name: str) -> LookupDictionary:
        return LookupManager.dictionaries[name]

    @staticmethod
    def add_dictionaries_from_folder(path: str):
        for f in os.listdir(path):
            if f.endswith(".dic"):
                dict_path = os.path.join(path, f)
                new_dictionary = LookupManager.factory.read_from_file(
                    dict_path
                )
                if new_dictionary is None:
                    raise TwaddleDictionaryException(f"[LookupManager.add_dictionaries_from_folder] dictionary file {dict_path} could not be read. Are name and forms defined?")
                LookupManager.dictionaries[new_dictionary.name] = new_dictionary

    @staticmethod
    def clear_labels():
        for dictionary in LookupManager.dictionaries.values():
            dictionary.clear_labels()

    @staticmethod
    def do_lookup(lookup: LookupObject):
        dictionary: LookupDictionary = LookupManager[lookup.dictionary]
        return dictionary.get(lookup)