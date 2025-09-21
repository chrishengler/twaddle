from collections import OrderedDict
from random import choice

from twaddle.compiler.compiler_objects import IndefiniteArticleObject, LookupObject
from twaddle.exceptions import TwaddleLookupException
from twaddle.lookup.lookup_entry import DictionaryEntry


class LookupDictionary:
    special_tokens = {"{a}": IndefiniteArticleObject()}

    def __init__(self, name: str, forms: list[str]):
        self.name = name
        self.forms = forms
        self.entries = list[DictionaryEntry]()
        self.labels = dict[str, DictionaryEntry]()
        self.tags = list[str]()

    def add(self, forms: list[str], tags: set[str] = None):
        if len(forms) != len(self.forms):
            raise TwaddleLookupException(
                "[LookupDictionary.add] wrong number of forms provided"
            )
        entry = DictionaryEntry(OrderedDict(zip(self.forms, forms)), tags)
        if tags:
            for tag in tags:
                if tag not in self.tags:
                    self.tags.append(tag)
        self.entries.append(entry)

    def clear_labels(self):
        self.labels = dict[str, DictionaryEntry]()

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
        lookup: LookupObject,
    ) -> list[DictionaryEntry]:
        valid_choices = list[DictionaryEntry]()
        for entry in self.entries:
            if entry.has_any_tag_of(lookup.negative_tags):
                continue
            if not lookup.positive_tags or entry.has_all_tags(lookup.positive_tags):
                valid_choices.append(entry)
        if not valid_choices and not lookup.strict_mode:
            valid_choices = list.copy(self.entries)
        valid_choices = self._prune_valid_choices(valid_choices, lookup.negative_labels)
        return valid_choices

    def _prune_valid_choices(
        self, valid_choices: list[DictionaryEntry], labels_negative: set[str]
    ) -> list[DictionaryEntry]:
        if labels_negative:
            for label in labels_negative:
                if label in self.labels and self.labels[label] in valid_choices:
                    valid_choices.remove(self.labels[label])
        return valid_choices

    def _get(self, lookup: LookupObject) -> str:
        lookup.form = self._get_form(lookup.form)
        if lookup.positive_label and lookup.positive_label in self.labels:
            return self.labels[lookup.positive_label][lookup.form]

        valid_choices = self._get_valid_choices(lookup)

        chosen_entry = choice(valid_choices)
        if lookup.positive_label:
            self.labels[lookup.positive_label] = chosen_entry
        return chosen_entry[lookup.form]

    def get(self, lookup: LookupObject) -> str | IndefiniteArticleObject:
        if lookup.strict_mode and (lookup.positive_tags or lookup.negative_tags):
            all_tags = list()
            if lookup.positive_tags:
                for tag in lookup.positive_tags:
                    all_tags.append(tag)
            if lookup.negative_tags:
                for tag in lookup.negative_tags:
                    all_tags.append(tag)
            for tag in all_tags:
                if tag not in self.tags:
                    raise TwaddleLookupException(
                        f"[LookupDictionary._get] Invalid class '{tag}' requested "
                        f"for dictionary '{self.name}' in strict mode"
                    )

        result = self._get(lookup)
        if result in self.special_tokens:
            return self.special_tokens[result]
        return result
