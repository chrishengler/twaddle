from rant.rant import Rant
import os

def relative_path_to_full_path(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, rel_path)

path = relative_path_to_full_path("../resources")
r = Rant(path)

def test_rant():
    assert r.run_sentence("hello world") == "hello world"

def test_rant_with_lookups():
    assert r.run_sentence("hello <adj> world") == "hello happy world"
    assert r.run_sentence("hello, welcome to my <adj> <noun-building-!small>") == "hello, welcome to my happy factory"

def test_rant_with_labels():
    assert r.run_sentence("big <noun-building-large::=a>, small <noun-building::!=a>") == "big factory, small shed"
    assert r.run_sentence("my <noun-shape::=a> is a regular <noun::=a>") == "my hexagon is a regular hexagon"


if __name__ == "__main__":
    test_rant()
