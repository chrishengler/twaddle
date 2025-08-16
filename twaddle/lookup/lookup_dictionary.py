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

    def add(self, forms: list[str], tags: set[str] = None):
        if len(forms) != len(self.forms):
            raise TwaddleLookupException(
                "[LookupDictionary.add] wrong number of forms provided"
            )
        lookup = DictionaryEntry(OrderedDict(zip(self.forms, forms)), tags)
        self.entries.append(lookup)

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
        tags_positive: set[str] = None,
        tags_negative: set[str] = None,
        labels_negative: set[str] = None,
    ) -> list[DictionaryEntry]:
        valid_choices = list[DictionaryEntry]()
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
        self, valid_choices: list[DictionaryEntry], labels_negative: set[str]
    ) -> list[DictionaryEntry]:
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

    def get(self, lookup: LookupObject) -> str | IndefiniteArticleObject:
        result = self._get(
            lookup.form,
            lookup.positive_tags,
            lookup.negative_tags,
            lookup.positive_label,
            lookup.negative_labels,
        )
        if result in self.special_tokens:
            return self.special_tokens[result]
        return result
