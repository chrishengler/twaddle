from collections import OrderedDict
from random import choice
from rant_exceptions import RantLookupException

class LookupEntry:
    def __init__(self, forms: OrderedDict[str,str], tags: set[str] = None):
        self.forms = forms
        self.tags = tags

    def __getitem__(self, form: str):
        return self.forms[form]

    def has_any_tag_of(self, tags: set[str]) -> bool:
        if tags is None or self.tags is None:
            return False
        return not self.tags.isdisjoint(tags)

class LookupDictionary:
    def __init__(self, name: str, forms: list[str]):
        self.name = name
        self.forms = forms
        self.entries = list[LookupEntry]()

    def add(self, forms: list[str], tags: set[str] = None):
        if len(forms) != len(self.forms):
            raise RantLookupException("[LookupDictionary.add] wrong number of forms provided")
        lookup = LookupEntry(OrderedDict(zip(self.forms, forms)), tags)
        self.entries.append(lookup)

    def get(self, form: str, tags_positive: set[str] = None, tags_negative: set[str] = None) -> str:
        if form not in self.forms:
            raise RantLookupException(f"[LookupDictionary.get] dictionary '{self.name}' has no form '{form}'")
        valid_choices = list[LookupEntry]()
        if not tags_negative  and not tags_positive:
            valid_choices = self.entries
        else:
            for entry in self.entries:
                valid = False
                if not tags_positive or entry.has_any_tag_of(tags_positive):
                    valid = True
                if entry.has_any_tag_of(tags_negative):
                    valid = False
                if valid:
                    valid_choices.append(entry)
        if not valid_choices:
            valid_choices = self.entries
        return choice(valid_choices)[form]

