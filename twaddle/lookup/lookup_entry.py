from collections import OrderedDict


class DictionaryEntry:
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
