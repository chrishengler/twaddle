import os

from twaddle.runner import TwaddleRunner


def relative_path_to_full_path(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, rel_path)


path = relative_path_to_full_path("../resources/valid_dicts")
r = TwaddleRunner(path)


def test_rant():
    assert r.run_sentence("hello world") == "hello world"


def test_lookups():
    assert r.run_sentence("hello <adj> world") == "hello happy world"
    assert (
        r.run_sentence("hello, welcome to my <adj> <noun-building-!small>")
        == "hello, welcome to my happy factory"
    )


def test_lookups_with_labels():
    assert (
        r.run_sentence("big <noun-building-large::=a>, small <noun-building::!=a>")
        == "big factory, small shed"
    )
    assert (
        r.run_sentence("my <noun-shape::=a> is a regular <noun::=a>")
        == "my hexagon is a regular hexagon"
    )


# noinspection SpellCheckingInspection
def test_repetition():
    assert r.run_sentence("[rep:3]{<noun-shape>}") == "hexagonhexagonhexagon"


def test_repetition_with_separator():
    assert r.run_sentence("[rep:3][sep: ]{hey}") == "hey hey hey"


def test_repetition_with_first():
    assert (
        r.run_sentence("[rep:3][sep:! ][first:give me ]{more}!")
        == "give me more! more! more!"
    )


def test_repetition_with_last():
    assert r.run_sentence("[rep:3][sep:, ][last:, and ]{no}") == "no, no, and no"


def test_repetition_with_article_in_args():
    assert (
        r.run_sentence(r"[rep:3][sep:, \a ][first:\a ][last:, and \a ]{<noun-vehicle>}")
        == "an ambulance, an ambulance, and an ambulance"
    )


def test_indefinite_article():
    assert r.run_sentence("\\a bow and \\A arrow") == "a bow and An arrow"
    assert r.run_sentence("[case:title]\\a bow and \\a arrow") == "A Bow And An Arrow"
    assert r.run_sentence("[case:upper]\\a bow and \\a arrow") == "A BOW AND AN ARROW"


def test_escaped_characters():
    assert r.run_sentence("\<hey\>\{\}") == "<hey>{}"


# noinspection SpellCheckingInspection,PyPep8
def test_regex():
    assert r.run_sentence("[//a//i:a;\\a <noun-shape>]") == "a hexagon"
    assert (
        r.run_sentence("[//hexagon//:hexagon;a [match] has 6 sides]")
        == "a hexagon has 6 sides"
    )
    assert r.run_sentence("[//^\w\w[aou]?//i:this;{[match]tab}]") == "thtabis"
    assert (
        r.run_sentence("[//tab.*//i:[//^\w\w[aou]?//i:this;{[match]tab}];tab]")
        == "thtab"
    )


def test_assign_tags_in_hidden_block():
    assert (
        r.run_sentence(
            r"[hide]{<noun-shape::=a><noun-animal::=b><noun-vehicle::=c>}"
            "<noun::=b> <noun::=a> <noun::=c>"
        )
        == "dog hexagon ambulance"
    )


# noinspection SpellCheckingInspection,PyPep8
def test_complex_sentence():
    assert r.run_sentence("[rep:2]{[//[aeiou]//:<noun-shape>;o]}") == "hoxogonhoxogon"
    assert (
        r.run_sentence(
            "[case:title]the <noun-building-small::=a> and \\a [//hat//:hat;<noun-building::!=a>]"
        )
        == "The Shed And A Factory"
    )
    assert (
        r.run_sentence("[//s\w//:suspicious slimy slithery snakes;ss[match]]")
        == "sssussspicious ssslimy ssslithery sssnakes"
    )
    assert (
        r.run_sentence("[//[3-5]//:[rep:3][sep:\\n]{123456};x]")
        == """12xxx6
12xxx6
12xxx6"""
    )


def test_indefinite_article_at_block_end():
    assert r.run_sentence("{\\a} cat and {\\a} egg") == "a cat and an egg"


if __name__ == "__main__":
    test_regex()
