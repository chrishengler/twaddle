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
    lookup = LookupObject(dictionary="noun", form="singular")
    assert dictionary._get(lookup) == "hexagon"
    lookup.form = "plural"
    assert dictionary._get(lookup) == "hexagons"
    with pytest.raises(TwaddleLookupException) as e_info:
        lookup.form = "invalid"
        dictionary._get(lookup)
    assert (
        e_info.value.message
        == "[LookupDictionary.get] dictionary 'noun' has no form 'invalid'"
    )


def test_tag_requirement():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], {"tag1"})
    dictionary.add(["hexagon", "hexagons"], {"tag2"})
    for _ in range(0, 5):
        lookup = LookupObject("noun")
        lookup.form = "plural"
        lookup.positive_tags = {"tag1"}
        assert dictionary._get(lookup) == "things"
        lookup.form = "singular"
        lookup.positive_tags = {"tag2"}
        assert dictionary._get(lookup) == "hexagon"
        lookup.form = "plural"
        lookup.positive_tags = {}
        lookup.negative_tags = {"tag1"}
        assert dictionary._get(lookup) == "hexagons"


def test_label_positive():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], {"tag1"})
    dictionary.add(["hexagon", "hexagons"], {"tag2"})
    lookup = LookupObject(
        dictionary="noun",
        form="singular",
        positive_tags={"tag1"},
        positive_label="tests",
    )
    assert dictionary._get(lookup) == "thing"
    for _ in range(0, 5):
        lookup.positive_tags = {}
        assert dictionary._get(lookup) == "thing"


def test_labels_negative():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], {"tag1"})
    dictionary.add(["hexagon", "hexagons"], {"tag2"})
    positive_tag_lookup = LookupObject(
        dictionary="noun",
        form="singular",
        positive_tags={"tag1"},
        positive_label="tests",
    )
    assert dictionary._get(positive_tag_lookup) == "thing"
    for _ in range(0, 5):
        negative_tag_lookup = LookupObject(
            dictionary="noun", form="singular", negative_labels={"tests"}
        )
        assert dictionary._get(negative_tag_lookup) == "hexagon"
        # just to check no problems with undefined labels
        negative_tag_lookup.negative_labels = {"hat"}
        assert dictionary._get(negative_tag_lookup)
    dictionary.clear_labels()
    results_after_clearing = list[str]()
    for _ in range(0, 50):
        negative_tag_lookup = LookupObject(
            dictionary="noun", form="singular", negative_labels={"tests"}
        )
        results_after_clearing.append(dictionary._get(negative_tag_lookup))
    assert "thing" in results_after_clearing


def test_label_overwrite():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], {"tag1"})
    dictionary.add(["hexagon", "hexagons"], {"tag2"})
    first_positive_label_lookup = LookupObject(
        dictionary="noun",
        form="singular",
        positive_tags={"tag1"},
        positive_label="tests",
    )
    second_positive_label_lookup = LookupObject(
        dictionary="noun",
        form="singular",
        positive_tags={"tag1"},
        positive_label="moretests",
    )
    assert dictionary._get(first_positive_label_lookup) == "thing"
    assert dictionary._get(second_positive_label_lookup) == "thing"
    first_positive_label_lookup.positive_tags = {}
    second_positive_label_lookup.positive_tags = {}
    for _ in range(0, 5):
        assert dictionary._get(first_positive_label_lookup) == "thing"
        assert dictionary._get(second_positive_label_lookup) == "thing"
    redefine_label_lookup = LookupObject(
        dictionary="noun",
        form="singular",
        positive_tags={"tag2"},
        redefine_labels={"tests", "moretests"},
    )
    assert dictionary._get(redefine_label_lookup) == "hexagon"
    for _ in range(0, 5):
        assert dictionary._get(first_positive_label_lookup) == "hexagon"
        assert dictionary._get(second_positive_label_lookup) == "hexagon"


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
    lookup = LookupObject("adj")
    assert dictionary.name == "adj"
    assert dictionary.forms == ["adj", "ness"]
    assert dictionary._get(lookup) == "happy"
    lookup.form = "ness"
    assert dictionary._get(lookup) == "happiness"
    lookup.form = None
    assert dictionary._get(lookup) == "happy"


def test_dictionary_read_from_file_with_classes():
    factory = DictionaryFileParser()
    path = relative_path_to_full_path(
        "../resources/valid_dicts/example_with_classes.dic"
    )
    dictionary = factory.read_from_path(path)
    assert dictionary.name == "noun"
    assert dictionary.forms == ["singular", "plural"]
    lookup = LookupObject("noun", positive_tags={"shape"})
    assert dictionary._get(lookup) == "hexagon"
    lookup.positive_tags = {"animal"}
    assert dictionary._get(lookup) == "dog"
    lookup.positive_tags = {"building", "large"}
    assert dictionary._get(lookup) == "factory"


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
    assert len(lookup_manager.dictionaries) == 4
    noun_dictionary: LookupDictionary = lookup_manager["noun"]
    adj_dictionary: LookupDictionary = lookup_manager["adj"]
    lookup = LookupObject("noun", form="plural", positive_tags={"shape"})
    assert noun_dictionary._get(lookup) == "hexagons"
    lookup = LookupObject("adj")
    assert adj_dictionary._get(lookup) == "happy"


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


def test_strict_lookup_invalid_tags():
    path = relative_path_to_full_path("../resources/valid_dicts")
    lookup_manager = LookupManager()
    lookup_manager.add_dictionaries_from_folder(path)
    invalid_pos_lookup = LookupObject(
        "noun", positive_tags={"invalid"}, strict_mode=True
    )
    invalid_neg_lookup = LookupObject(
        "noun", negative_tags={"invalid"}, strict_mode=True
    )
    invalid_with_valid = LookupObject(
        "noun", positive_tags={"shape", "invalid"}, strict_mode=True
    )
    invalid_with_valid_separate = LookupObject(
        "noun", positive_tags={"shape"}, negative_tags={"invalid"}, strict_mode=True
    )
    for lookup in [
        invalid_pos_lookup,
        invalid_neg_lookup,
        invalid_with_valid,
        invalid_with_valid_separate,
    ]:
        with pytest.raises(TwaddleLookupException) as e_info:
            lookup_manager.do_lookup(lookup)
        assert (
            e_info.value.message
            == "[LookupDictionary._strict_class_validation] Invalid class 'invalid'"
            " requested for dictionary 'noun' in strict mode"
        )


def test_lookup_antimatch_undefined_label():
    path = relative_path_to_full_path("../resources/valid_dicts")
    lookup_manager = LookupManager()
    lookup_manager.add_dictionaries_from_folder(path)
    strict_lookup = LookupObject(
        "noun", negative_labels={"undefined"}, strict_mode=True
    )
    with pytest.raises(TwaddleLookupException) as e_info:
        lookup_manager.do_lookup(strict_lookup)
    assert (
        e_info.value.message
        == "[LookupDictionary._strict_label_validation] Requested antimatch of label "
        "'undefined', not defined for dictionary 'noun'"
    )


def test_standard_compiler_prints_something_when_antimatch_exhausts_all_options():
    path = relative_path_to_full_path("../resources/valid_dicts")
    lookup_manager = LookupManager()
    lookup_manager.add_dictionaries_from_folder(path)
    lookup = LookupObject("noun", positive_tags={"shape"}, positive_label="a")
    assert lookup_manager.do_lookup(lookup) == "hexagon"
    lookup = LookupObject("noun", positive_tags={"shape"}, negative_labels={"a"})
    # result is random and arbitrary, simply ensure no exception is raised
    # and that _something_ is returned
    value = lookup_manager.do_lookup(lookup)
    assert value is not None


def test_strict_compiler_raises_when_antimatch_exhausts_all_options():
    path = relative_path_to_full_path("../resources/valid_dicts")
    lookup_manager = LookupManager()
    lookup_manager.add_dictionaries_from_folder(path)
    lookup = LookupObject("noun", positive_tags={"shape"}, positive_label="a")
    assert lookup_manager.do_lookup(lookup) == "hexagon"
    strict_lookup = LookupObject(
        "noun", positive_tags={"shape"}, negative_labels={"a"}, strict_mode=True
    )
    with pytest.raises(TwaddleLookupException) as e_info:
        lookup_manager.do_lookup(strict_lookup)
    assert (
        e_info.value.message
        == "[LookupDictionary._valid_choices_for_strictness_level] no valid choices for"
        " strict mode lookup in dictionary 'noun'"
    )


if __name__ == "__main__":
    test_lookup_from_object()
