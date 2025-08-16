import os
from pathlib import Path

import pytest

from twaddle.compiler.compiler_objects import IndefiniteArticleObject
from twaddle.exceptions import TwaddleDictionaryException, TwaddleLookupException
from twaddle.lookup.dictionary_file_parser import DictionaryFileParser
from twaddle.lookup.lookup_dictionary import LookupDictionary, LookupObject
from twaddle.lookup.lookup_entry import DictionaryEntry
from twaddle.lookup.lookup_manager import LookupManager


def relative_path_to_full_path(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return Path(os.path.join(current_dir, rel_path))


# noinspection SpellCheckingInspection
def test_lookup_type():
    lookup_thing = DictionaryEntry(
        {
            "singular": "thing",
            "plural": "things",
            "possessive": "thing's",
            "pluralpossessive": "things'",
        }
    )
    assert lookup_thing["singular"] == "thing"
    assert lookup_thing["plural"] == "things"
    assert lookup_thing["possessive"] == "thing's"
    assert lookup_thing["pluralpossessive"] == "things'"


def test_dictionary():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["hexagon", "hexagons"])
    assert len(dictionary.entries) == 1
    assert dictionary._get("singular") == "hexagon"
    assert dictionary._get("plural") == "hexagons"
    with pytest.raises(TwaddleLookupException) as e_info:
        dictionary._get("invalid")
        assert (
            e_info.message
            == "[LookupDictionary.get] dictionary 'noun' has no form 'invalid'"
        )


def test_tag_requirement():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], {"tag1"})
    dictionary.add(["hexagon", "hexagons"], {"tag2"})
    for _ in range(0, 5):
        assert dictionary._get("plural", {"tag1"}) == "things"
        assert dictionary._get("singular", {"tag2"}) == "hexagon"
        assert dictionary._get("plural", set(), {"tag1"}) == "hexagons"


def test_label_positive():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], {"tag1"})
    dictionary.add(["hexagon", "hexagons"], {"tag2"})
    assert dictionary._get("singular", {"tag1"}, set(), "tests") == "thing"
    for _ in range(0, 5):
        assert dictionary._get("singular", set(), set(), "tests") == "thing"


def test_labels_negative():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], {"tag1"})
    dictionary.add(["hexagon", "hexagons"], {"tag2"})
    assert dictionary._get("singular", {"tag1"}, set(), "tests") == "thing"
    for _ in range(0, 5):
        assert dictionary._get("singular", set(), set(), None, {"tests"}) == "hexagon"
        # just to check no problems with undefined labels
        assert dictionary._get("singular", set(), set(), None, {"hat"})
    dictionary.clear_labels()
    results_after_clearing = list[str]()
    for _ in range(0, 50):
        results_after_clearing.append(
            dictionary._get("singular", set(), set(), None, {"tests"})
        )
    assert "thing" in results_after_clearing


def test_dictionary_attributes_from_lines():
    factory = DictionaryFileParser()
    name = factory.read_name("#name noun")
    assert name == "noun"
    forms = factory.read_forms("#subs singular plural")
    assert forms == ["singular", "plural"]
    forms = factory.read_forms("#forms singular plural")
    assert forms == ["singular", "plural"]


def test_dictionary_read_from_file_simple():
    factory = DictionaryFileParser()
    path = relative_path_to_full_path("../resources/valid_dicts/example.dic")
    dictionary = factory.read_from_path(path)
    assert dictionary.name == "adj"
    assert dictionary.forms == ["adj", "ness"]
    assert dictionary._get("adj") == "happy"
    assert dictionary._get("ness") == "happiness"
    assert dictionary._get() == "happy"


def test_dictionary_read_from_file_with_classes():
    factory = DictionaryFileParser()
    path = relative_path_to_full_path(
        "../resources/valid_dicts/example_with_classes.dic"
    )
    dictionary = factory.read_from_path(path)
    assert dictionary.name == "noun"
    assert dictionary.forms == ["singular", "plural"]
    assert dictionary._get("singular", {"shape"}) == "hexagon"
    assert dictionary._get("plural", {"animal"}) == "dogs"
    assert dictionary._get("singular", {"building", "large"}) == "factory"


def test_load_empty_file_raise_exception():
    path = relative_path_to_full_path("../resources/invalid_dicts/empty")
    with pytest.raises(
        TwaddleDictionaryException, match=r".*empty.dic could not be read.*"
    ):
        lookup_manager = LookupManager()
        lookup_manager.add_dictionaries_from_folder(path)
        assert len(lookup_manager.dictionaries) == 0


def test_load_file_no_forms_raise_exception():
    path = relative_path_to_full_path("../resources/invalid_dicts/no_forms")
    with pytest.raises(
        TwaddleDictionaryException, match=r".*no_forms.dic could not be read.*"
    ):
        lookup_manager = LookupManager()
        lookup_manager.add_dictionaries_from_folder(path)
        assert len(lookup_manager.dictionaries) == 0


def test_load_file_no_header_raise_exception():
    path = relative_path_to_full_path("../resources/invalid_dicts/no_header")
    with pytest.raises(
        TwaddleDictionaryException, match=r".*content_no_header.dic could not be read.*"
    ):
        lookup_manager = LookupManager()
        lookup_manager.add_dictionaries_from_folder(path)
        assert len(lookup_manager.dictionaries) == 0


def test_dictionary_manager():
    path = relative_path_to_full_path("../resources/valid_dicts")
    lookup_manager = LookupManager()
    lookup_manager.add_dictionaries_from_folder(path)
    assert len(lookup_manager.dictionaries) == 3
    noun_dictionary: LookupDictionary = lookup_manager["noun"]
    adj_dictionary: LookupDictionary = lookup_manager["adj"]
    assert noun_dictionary._get("plural", {"shape"}) == "hexagons"
    assert adj_dictionary._get() == "happy"


def test_lookup_from_object():
    path = relative_path_to_full_path("../resources/valid_dicts")
    lookup_manager = LookupManager()
    lookup_manager.add_dictionaries_from_folder(path)
    lookup = LookupObject("adj")
    assert lookup_manager.do_lookup(lookup) == "happy"


def test_lookup_indefinite_article():
    path = relative_path_to_full_path("../resources/valid_dicts")
    lookup_manager = LookupManager()
    lookup_manager.add_dictionaries_from_folder(path)
    lookup = LookupObject("article", form="indefinite")
    result = lookup_manager.do_lookup(lookup)
    assert isinstance(result, IndefiniteArticleObject)


if __name__ == "__main__":
    test_lookup_from_object()
