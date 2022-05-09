from collections import OrderedDict
from random import choice
from rant_exceptions import RantLookupException

class LookupEntry:
    def __init__(self, forms: OrderedDict[str,str]):
        self.forms = forms

    def __getitem__(self, form: str):
        return self.forms[form]

class LookupDictionary:
    def __init__(self, name: str, forms: list[str]):
        self.name = name
        self.forms = forms
        self.entries = list[LookupEntry]()

    def add(self, entry: LookupEntry):
        self.entries.append(entry)

    def get(self, form: str):
        if form not in self.forms:
            raise RantLookupException(f"[LookupDictionary.get] dictionary '{self.name}' has no form '{form}'")
        return choice(self.entries)[form]
