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

    def _valid_choices_for_strictness_level(
        self,
        valid_choices: list[DictionaryEntry],
        lookup: LookupObject,
    ) -> list[DictionaryEntry]:
        if not valid_choices:
            if lookup.strict_mode:
                raise TwaddleLookupException(
                    "[LookupDictionary._valid_choices_for_strictness_level] "
                    f"no valid choices for strict mode lookup in dictionary '{self.name}'"
                )
            valid_choices = list.copy(self.entries)
        return valid_choices

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
        valid_choices = self._valid_choices_for_strictness_level(valid_choices, lookup)
        valid_choices = self._prune_valid_choices(valid_choices, lookup.negative_labels)
        valid_choices = self._valid_choices_for_strictness_level(valid_choices, lookup)
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
        if lookup.redefine_labels:
            for label in lookup.redefine_labels:
                self.labels[label] = chosen_entry
        elif lookup.positive_label:
            self.labels[lookup.positive_label] = chosen_entry
        return chosen_entry[lookup.form]

    def _strict_class_validation(self, lookup: LookupObject):
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
                    f"[LookupDictionary._strict_class_validation] Invalid class '{tag}' requested "
                    f"for dictionary '{self.name}' in strict mode"
                )

    def _strict_label_validation(self, lookup: LookupObject):
        if lookup.negative_labels:
            for label in lookup.negative_labels:
                if label not in self.labels:
                    raise TwaddleLookupException(
                        "[LookupDictionary._strict_label_validation] Requested antimatch of label "
                        f"'{label}', not defined for dictionary '{self.name}'"
                    )

    def _validate_strict_mode(self, lookup: LookupObject):
        if not lookup.strict_mode:
            return
        self._strict_class_validation(lookup)
        self._strict_label_validation(lookup)

    def get(self, lookup: LookupObject) -> str | IndefiniteArticleObject:
        self._validate_strict_mode(lookup)
        result = self._get(lookup)
        if result in self.special_tokens:
            return self.special_tokens[result]
        return result
