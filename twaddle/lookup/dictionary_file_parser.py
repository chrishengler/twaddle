from importlib.resources.abc import Traversable
from pathlib import Path

from twaddle.lookup.lookup_dictionary import LookupDictionary


class DictionaryFileParser:
    @staticmethod
    def read_forms(forms_line: str) -> list[str]:
        return forms_line.split()[1:]

    @staticmethod
    def read_name(name_line: str) -> str:
        return name_line.split()[1]

    @staticmethod
    def read_entry(entry_line: str) -> list[str]:
        return entry_line.split("/")

    @staticmethod
    def read_from_path(path: str | Path | Traversable) -> LookupDictionary | None:
        if not isinstance(path, Path):
            path = Path(path) if isinstance(path, str) else Path(str(path))
        with path.open("r", encoding="utf-8") as input_file:
            name: str | None = None
            forms: list[str] | None = None
            dictionary: LookupDictionary | None = None
            classes: set[str] = set()
            for line in input_file:
                if dictionary is None:
                    if not name:
                        name = DictionaryFileParser._try_read_name(line)
                    if not forms:
                        forms = DictionaryFileParser._try_read_forms(line)
                    if name and forms:
                        dictionary = LookupDictionary(name, forms)
                else:
                    # purely to shut up pylance, dictionary is only set once forms has a value
                    # so we can't reach here if forms is None
                    assert forms is not None
                    DictionaryFileParser._read_line(line, forms, classes, dictionary)
            return dictionary

    @staticmethod
    def _try_read_name(line: str) -> str | None:
        name = None
        if line.startswith("#name"):
            name = DictionaryFileParser.read_name(line)
        return name

    @staticmethod
    def _try_read_forms(line: str) -> list[str] | None:
        forms = None
        if line.startswith("#forms") or line.startswith("#subs"):
            forms = DictionaryFileParser.read_forms(line)
        return forms

    @staticmethod
    def _read_line(
        line: str,
        forms: list[str],
        classes: set[str],
        dictionary: LookupDictionary,
    ):
        line = line.strip()
        if line.startswith("#class add"):
            classes.add(line.split()[-1])
        elif line.startswith("#class remove") and line.split()[-1] in classes:
            classes.remove(line.split()[-1])
        elif line.startswith("> "):
            line = line[2:]
            entry = DictionaryFileParser.read_entry(line)
            if len(entry) == len(forms):
                dictionary.add(entry, classes.copy())
