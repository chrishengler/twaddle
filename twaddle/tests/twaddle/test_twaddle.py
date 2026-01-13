import os

import pytest

from twaddle.exceptions import TwaddleLookupException
from twaddle.runner import TwaddleRunner


def relative_path_to_full_path(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, rel_path)


path = relative_path_to_full_path("../resources/valid_dicts")
standard_runner = TwaddleRunner(path)
strict_runner = TwaddleRunner(path, strict_mode=True)


def test_rant():
    assert standard_runner.run_sentence("hello world") == "hello world"


def test_lookups():
    assert standard_runner.run_sentence("hello <adj> world") == "hello happy world"
    assert (
        standard_runner.run_sentence(
            "hello, welcome to my <adj> <noun-building-!small>"
        )
        == "hello, welcome to my happy factory"
    )


def test_lookups_with_labels():
    assert (
        standard_runner.run_sentence(
            "big <noun-building-large::=a>, small <noun-building::!=a>"
        )
        == "big factory, small shed"
    )
    assert (
        standard_runner.run_sentence("my <noun-shape::=a> is a regular <noun::=a>")
        == "my hexagon is a regular hexagon"
    )


def test_persistent_lookups_with_labels():
    persistent_runner = TwaddleRunner(path, persistent=True)
    assert (
        persistent_runner.run_sentence(
            "big <noun-building-large::=a>, small <noun-building::!=a>"
        )
        == "big factory, small shed"
    )
    assert persistent_runner.run_sentence("<noun::=a>") == "factory"
    assert persistent_runner.run_sentence("<noun-building::!=a>") == "shed"


def test_clearing_lookup_labels():
    persistent_runner = TwaddleRunner(path, persistent=True)
    assert (
        persistent_runner.run_sentence(
            "big <noun-building-large::=a>, small <noun-building::!=a>"
        )
        == "big factory, small shed"
    )
    results = []
    for _ in range(0, 10):
        persistent_runner.clear()
        results.append(persistent_runner.run_sentence("<noun::=a>"))
    assert len(set(results)) > 1


def test_clearing_lookup_labels_in_sentence():
    persistent_runner = TwaddleRunner(path, persistent=True)
    assert (
        persistent_runner.run_sentence(
            "big <noun-building-large::=a>, small <noun-building::!=a>"
        )
        == "big factory, small shed"
    )
    results = []
    for _ in range(0, 10):
        results.append(persistent_runner.run_sentence("[clear]<noun::=a>"))
    assert len(set(results)) > 1
    results = []
    for _ in range(0, 10):
        results.append(
            persistent_runner.run_sentence(r"<noun-shape::=a>[clear]<noun::=a>")
        )
    assert len(set(results)) > 1


# noinspection SpellCheckingInspection
def test_repetition():
    assert (
        standard_runner.run_sentence("[rep:3]{<noun-shape>}") == "hexagonhexagonhexagon"
    )


def test_repetition_with_separator():
    assert standard_runner.run_sentence("[rep:3][sep: ]{hey}") == "hey hey hey"


def test_repetition_with_first():
    assert (
        standard_runner.run_sentence("[rep:3][sep:! ][first:give me ]{more}!")
        == "give me more! more! more!"
    )


def test_repetition_with_last():
    assert (
        standard_runner.run_sentence("[rep:3][sep:, ][last:, and ]{no}")
        == "no, no, and no"
    )


def test_repetition_with_article_in_args():
    assert (
        standard_runner.run_sentence(
            r"[rep:3][sep:, \a ][first:\a ][last:, and \a ]{<noun-vehicle>}"
        )
        == "an ambulance, an ambulance, and an ambulance"
    )


def test_indefinite_article():
    assert standard_runner.run_sentence("\\a bow and \\A arrow") == "a bow and An arrow"
    assert (
        standard_runner.run_sentence("[case:title]\\a bow and \\a arrow")
        == "A Bow And An Arrow"
    )
    assert (
        standard_runner.run_sentence("[case:upper]\\a bow and \\a arrow")
        == "A BOW AND AN ARROW"
    )


def test_sentence_case_with_first_person_pronoun():
    assert (
        standard_runner.run_sentence(
            "[case:sentence]i don't know if <pronoun> care, <pronoun.lower> guess i do"
        )
        == "I don't know if I care, i guess I do"
    )


def test_escaped_characters():
    assert standard_runner.run_sentence("\<hey\>\{\}") == "<hey>{}"


def test_label_only_persistence():
    label_only_runner = TwaddleRunner(path, persistent_labels=True)

    assert (
        label_only_runner.run_sentence(
            "big <noun-building-large::=a>, small <noun-building::!=a>"
        )
        == "big factory, small shed"
    )
    assert label_only_runner.run_sentence("<noun::=a>") == "factory"

    sync_sentence = "[sync:test;locked]{a|b|c}"
    sync_results = [label_only_runner.run_sentence(sync_sentence)]
    for _ in range(0, 10):
        sync_results.append(label_only_runner.run_sentence(sync_sentence))
    assert len(set(sync_results)) > 1


def test_synchronizer_only_persistence():
    sync_only_runner = TwaddleRunner(path, persistent_synchronizers=True)

    first = sync_only_runner.run_sentence("[sync:test;locked]{a|b|c}")
    second = sync_only_runner.run_sentence("[sync:test;locked]{a|b|c}")
    assert first == second

    sync_only_runner.run_sentence(
        "big <noun-building-large::=a>, small <noun-building::!=a>"
    )
    results = [sync_only_runner.run_sentence("<noun::=a>")]
    for _ in range(0, 10):
        results.append(sync_only_runner.run_sentence("<noun::=a>"))
    assert len(set(results)) > 1


def test_persistence_overrides():
    runner = TwaddleRunner(
        path, persistent=True, persistent_labels=False, persistent_synchronizers=False
    )

    assert (
        runner.run_sentence("big <noun-building-large::=a>, small <noun-building::!=a>")
        == "big factory, small shed"
    )
    assert runner.run_sentence("<noun::=a>") == "factory"

    first = runner.run_sentence("[sync:test;locked]{a|b|c}")
    second = runner.run_sentence("[sync:test;locked]{a|b|c}")
    assert first == second


def test_patter_persistence():
    pattern_persistent_runner = TwaddleRunner(path, persistent_patterns=True)

    first = pattern_persistent_runner.run_sentence("[save:a]{<noun-vehicle>}")
    second = pattern_persistent_runner.run_sentence("[load:a]")

    assert first == second


# noinspection SpellCheckingInspection,PyPep8
def test_regex():
    assert standard_runner.run_sentence("[//a//i:a;\\a <noun-shape>]") == "a hexagon"
    assert (
        standard_runner.run_sentence("[//hexagon//:hexagon;a [match] has 6 sides]")
        == "a hexagon has 6 sides"
    )
    assert (
        standard_runner.run_sentence("[//^\w\w[aou]?//i:this;{[match]tab}]")
        == "thtabis"
    )
    assert (
        standard_runner.run_sentence(
            "[//tab.*//i:[//^\w\w[aou]?//i:this;{[match]tab}];tab]"
        )
        == "thtab"
    )


def test_assign_tags_in_hidden_block():
    assert (
        standard_runner.run_sentence(
            r"[hide]{<noun-shape::=a><noun-animal::=b><noun-vehicle::=c>}"
            "<noun::=b> <noun::=a> <noun::=c>"
        )
        == "dog hexagon ambulance"
    )


# noinspection SpellCheckingInspection,PyPep8
def test_complex_sentence():
    assert (
        standard_runner.run_sentence("[rep:2]{[//[aeiou]//:<noun-shape>;o]}")
        == "hoxogonhoxogon"
    )
    assert (
        standard_runner.run_sentence(
            "[case:title]the <noun-building-small::=a> and \\a [//hat//:hat;<noun-building::!=a>]"
        )
        == "The Shed And A Factory"
    )
    assert (
        standard_runner.run_sentence(
            "[//s\w//:suspicious slimy slithery snakes;ss[match]]"
        )
        == "sssussspicious ssslimy ssslithery sssnakes"
    )
    assert (
        standard_runner.run_sentence("[//[3-5]//:[rep:3][sep:\\n]{123456};x]")
        == """12xxx6
12xxx6
12xxx6"""
    )


def test_indefinite_article_at_block_end():
    assert standard_runner.run_sentence("{\\a} cat and {\\a} egg") == "a cat and an egg"


def test_indefinite_article_from_lookup():
    assert (
        standard_runner.run_sentence(
            "[case:sentence]<article.indefinite> cat and <article.indefinite> aardvark"
        )
        == "A cat and an aardvark"
    )


def test_strict_mode_error_invalid_class():
    with pytest.raises(TwaddleLookupException) as e_info:
        strict_runner.run_sentence("<noun-notarealclass>")
    assert (
        e_info.value.message
        == "[LookupDictionary._strict_class_validation] Invalid class 'notarealclass' requested "
        "for dictionary 'noun' in strict mode"
    )


def test_strict_mode_undefined_label():
    with pytest.raises(TwaddleLookupException) as e_info:
        strict_runner.run_sentence("<noun::!=undefined>")
    assert (
        e_info.value.message
        == "[LookupDictionary._strict_label_validation] Requested antimatch of label "
        "'undefined', not defined for dictionary 'noun'"
    )


def test_reverse_with_lookups():
    assert strict_runner.run_sentence("[reverse]{<noun-vehicle>}") == "ecnalubma"


def test_save_load_block_with_lookups():
    assert (
        standard_runner.run_sentence("[save:a]{<noun-vehicle>} [load:a]")
        == "ambulance ambulance"
    )


def test_save_load_block_with_reverse():
    assert (
        standard_runner.run_sentence("[save:a]{<noun-vehicle>} [reverse]{[load:a]}")
        == "ambulance ecnalubma"
    )


def test_save_load_with_case():
    assert (
        standard_runner.run_sentence(
            "[save:a]{<noun-vehicle>} [case:upper][reverse]{[load:a]}"
        )
        == "ambulance ECNALUBMA"
    )


def test_save_load_with_synchronizer():
    assert standard_runner.run_sentence("[save:a]{[sync:x;deck]{a|b}} [load:a]") in [
        "a b",
        "b a",
    ]


def test_save_effective_before_reverse():
    for sentence in [
        "[save:a][reverse]{abc} [load:a]",
        "[reverse][save:a]{abc} [load:a]",
        "[reverse]{[save:a]{abc}} [load:a]",
        "[save:a]{[reverse]{abc}} [reverse]{[load:a]}",
    ]:
        assert standard_runner.run_sentence(sentence) == "cba abc"


def test_copy_paste_with_lookups():
    assert (
        standard_runner.run_sentence("[copy:a]{<noun-vehicle>} [paste:a]")
        == "ambulance ambulance"
    )


def test_copy_load_block_with_reverse():
    assert (
        standard_runner.run_sentence("[copy:a]{<noun-vehicle>} [reverse]{[paste:a]}")
        == "ambulance ecnalubma"
    )


def test_copy_load_with_case():
    assert (
        standard_runner.run_sentence(
            "[copy:a]{<noun-vehicle>} [case:upper][reverse]{[paste:a]}"
        )
        == "ambulance ECNALUBMA"
    )


def test_copy_paste_with_synchronizer():
    assert standard_runner.run_sentence("[copy:a]{[sync:x;deck]{a|b}} [paste:a]") in [
        "a a",
        "b b",
    ]


def test_copy_effective_before_reverse():
    for sentence in [
        "[copy:a][reverse]{abc} [paste:a]",
        "[reverse][copy:a]{abc} [paste:a]",
        "[reverse]{[copy:a]{abc}} [paste:a]",
        "[copy:a]{[reverse]{abc}} [reverse]{[paste:a]}",
    ]:
        assert standard_runner.run_sentence(sentence) == "cba abc"


def test_calculation_with_stored_values():
    persistent_runner = TwaddleRunner(path, persistent=True)
    assert (
        persistent_runner.run_sentence("Keanu Reeves was born in [save:krbirth]{1964}.")
        == "Keanu Reeves was born in 1964."
    )
    assert (
        persistent_runner.run_sentence(
            "Point Break was released in [save:pbrelease]{1991}."
        )
        == "Point Break was released in 1991."
    )
    assert (
        persistent_runner.run_sentence(
            "At the time, he was about [sub:[load:pbrelease];[load:krbirth]] years old."
        )
        == "At the time, he was about 27 years old."
    )


def test_redefine_label():
    assert (
        standard_runner.run_sentence(
            "<noun-vehicle::=a> <noun::=a> <noun-shape::^=a> <noun::=a>"
        )
        == "ambulance ambulance hexagon hexagon"
    )


def test_redefine_with_negative_labels():
    assert (
        standard_runner.run_sentence(
            "<noun-building-small::=a> <noun-building::^=a::!=a> <noun-building::^=a::!=a>"
        )
        == "shed factory shed"
    )
