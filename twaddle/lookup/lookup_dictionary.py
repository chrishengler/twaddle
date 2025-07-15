from collections import OrderedDict
from random import choice

from twaddle.exceptions import TwaddleLookupException
from twaddle.lookup.lookup_entry import LookupEntry
from twaddle.parser.compiler_objects import LookupObject


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




