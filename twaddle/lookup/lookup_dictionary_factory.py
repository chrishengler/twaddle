from twaddle.lookup.lookup_dictionary import LookupDictionary


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