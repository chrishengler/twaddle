from rant.rant import Rant
import os


def relative_path_to_full_path(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, rel_path)


path = relative_path_to_full_path("../resources")
r = Rant(path)


def test_rant():
    assert r.run_sentence("hello world") == "hello world"


def test_lookups():
    assert r.run_sentence("hello <adj> world") == "hello happy world"
    assert r.run_sentence(
        "hello, welcome to my <adj> <noun-building-!small>") == "hello, welcome to my happy factory"


def test_lookups_with_labels():
    assert r.run_sentence(
        "big <noun-building-large::=a>, small <noun-building::!=a>") == "big factory, small shed"
    assert r.run_sentence(
        "my <noun-shape::=a> is a regular <noun::=a>") == "my hexagon is a regular hexagon"


def test_repetition():
    assert r.run_sentence("[rep:3]{<noun-shape>}") == "hexagonhexagonhexagon"


def test_indefinite_article():
    assert r.run_sentence("\\a bow and \\A arrow") == "a bow and An arrow"
    assert r.run_sentence(
        "[case:title]\\a bow and \\a arrow") == "A Bow And An Arrow"
    assert r.run_sentence(
        "[case:upper]\\a bow and \\a arrow") == "A BOW AND AN ARROW"

if __name__ == "__main__":
    test_indefinite_article()
