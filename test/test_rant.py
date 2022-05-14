from rant import Rant
import os

def relative_path_to_full_path(rel_path: str) -> str:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, rel_path)

def test_rant():
    path = relative_path_to_full_path("./resources")
    r = Rant(path)
    assert r.run_sentence("hello world") == "hello world"
    assert r.run_sentence("hello <adj> world") == "hello happy world"
