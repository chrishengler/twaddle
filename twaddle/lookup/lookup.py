import os
from collections import OrderedDict
from random import choice

from twaddle.exceptions import TwaddleLookupException
from twaddle.parser.compiler_objects import LookupObject


class LookupEntry:
    def __init__(self, forms: OrderedDict[str, str], tags: set[str] = None):
        self.forms = forms
        self.tags = tags

    def __getitem__(self, form: str):
        return self.forms[form]

    def has_any_tag_of(self, tags: set[str]) -> bool:
        if tags is None or self.tags is None:
            return False
        return not self.tags.isdisjoint(tags)

    def has_all_tags(self, tags: set[str]) -> bool:
        for tag in tags:
            if tag not in self.tags:
                return False
        return True


class LookupDictionary:
    def __init__(self, name: str, forms: list[str]):
        self.name = name
        self.forms = forms
        self.entries = list[LookupEntry]()
        self.labels = dict[str, LookupEntry]()

    def add(self, forms: list[str], tags: set[str] = None):
        if len(forms) != len(self.forms):
            raise TwaddleLookupException(
                "[LookupDictionary.add] wrong number of forms provided"
            )
        lookup = LookupEntry(OrderedDict(zip(self.forms, forms)), tags)
        self.entries.append(lookup)

    def clear_labels(self):
        self.labels = dict[str, LookupEntry]()

    def _get_form(self, form: str) -> str:
        if form is None:
            form = self.forms[0]
        if form not in self.forms:
            raise TwaddleLookupException(
                f"[LookupDictionary.get] dictionary '{self.name}' has no form '{form}'"
            )
        return form

    def _get_valid_choices(
        self,
        tags_positive: set[str] = None,
        tags_negative: set[str] = None,
        labels_negative: set[str] = None,
    ) -> list[LookupEntry]:
        valid_choices = list[LookupEntry]()
        for entry in self.entries:
            if entry.has_any_tag_of(tags_negative):
                continue
            if not tags_positive or entry.has_all_tags(tags_positive):
                valid_choices.append(entry)
        if not valid_choices:
            valid_choices = list.copy(self.entries)
        valid_choices = self._prune_valid_choices(valid_choices, labels_negative)
        return valid_choices

    def _prune_valid_choices(
        self, valid_choices: list[LookupEntry], labels_negative: set[str]
    ) -> list[LookupEntry]:
        if labels_negative:
            for label in labels_negative:
                if label in self.labels and self.labels[label] in valid_choices:
                    valid_choices.remove(self.labels[label])
        return valid_choices

    def _get(
        self,
        form: str = None,
        tags_positive: set[str] = None,
        tags_negative: set[str] = None,
        label_positive: str = None,
        labels_negative: set[str] = None,
    ) -> str:
        form = self._get_form(form)
        if label_positive and label_positive in self.labels:
            return self.labels[label_positive][form]

        valid_choices = self._get_valid_choices(
            tags_positive, tags_negative, labels_negative
        )

        chosen_entry = choice(valid_choices)
        if label_positive:
            self.labels[label_positive] = chosen_entry
        return chosen_entry[form]

    def get(self, lookup: LookupObject) -> str:
        return self._get(
            lookup.form,
            lookup.positive_tags,
            lookup.negative_tags,
            lookup.positive_label,
            lookup.negative_labels,
        )


class LookupDictionaryFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_forms(forms_line: str) -> list[str]:
        return forms_line.split()[1:]

    @staticmethod
    def get_name(name_line: str) -> str:
        return name_line.split()[1]

    @staticmethod
    def get_entry(entry_line: str) -> list[str]:
        return entry_line.split("/")

    def read_from_file(self, path: str) -> LookupDictionary:
        with open(path, encoding="utf-8") as input_file:
            name = str()
            forms = list[str]()
            dictionary = None
            classes = set[str]()
            for line in input_file:
                if dictionary is None:
                    if not name:
                        name = self._try_name(line)
                    if not forms:
                        forms = self._try_forms(line)
                    if name and forms:
                        dictionary = LookupDictionary(name, forms)
                else:
                    self._read_line(line, name, forms, classes, dictionary)
            return dictionary

    def _try_name(self, line: str) -> str:
        name = None
        if line.startswith("#name"):
            name = self.get_name(line)
        return name

    def _try_forms(self, line: str) -> list[str]:
        forms = None
        if line.startswith("#forms") or line.startswith("#subs"):
            forms = self.get_forms(line)
        return forms

    def _read_line(
        self,
        line: str,
        name: str,
        forms: list[str],
        classes: list[str],
        dictionary: LookupDictionary,
    ):
        line = line.strip()
        if line.startswith("#class add"):
            classes.add(line.split()[-1])
        elif line.startswith("#class remove") and line.split()[-1] in classes:
            classes.remove(line.split()[-1])
        elif line.startswith("> "):
            line = line[2:]
            entry = self.get_entry(line)
            if len(entry) == len(forms):
                dictionary.add(entry, set.copy(classes))


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
                new_dictionary = LookupManager.factory.read_from_file(
                    os.path.join(path, f)
                )
                LookupManager.dictionaries[new_dictionary.name] = new_dictionary

    @staticmethod
    def clear_labels():
        for dictionary in LookupManager.dictionaries.values():
            dictionary.clear_labels()

    @staticmethod
    def do_lookup(lookup: LookupObject):
        dictionary: LookupDictionary = LookupManager[lookup.dictionary]
        return dictionary.get(lookup)
