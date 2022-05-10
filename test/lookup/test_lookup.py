from rant_exceptions import RantLookupException
from lookup.lookup import *
import pytest

def test_lookup_type():
    lookup_thing = LookupEntry({"singular": "thing",
                                "plural": "things",
                                "possessive": "thing's",
                                "pluralpossessive": "things'"})
    assert lookup_thing["singular"] == "thing"
    assert lookup_thing["plural"] == "things"
    assert lookup_thing["possessive"] == "thing's"
    assert lookup_thing["pluralpossessive"] == "things'"

def test_dictionary():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["hexagon", "hexagons"])
    assert len(dictionary.entries) == 1
    assert dictionary.get("singular") == "hexagon"
    assert dictionary.get("plural") == "hexagons"
    with pytest.raises(RantLookupException) as e_info:
        dictionary.get("invalid")
        assert e_info.message == "[LookupDictionary.get] dictionary 'noun' has no form 'invalid'"

def test_tag_requirement():
    dictionary = LookupDictionary("noun", ["singular", "plural"])
    dictionary.add(["thing", "things"], set(["tag1"]))
    dictionary.add(["hexagon", "hexagons"], set(["tag2"]))
    for _ in range(0,5):
        assert dictionary.get("plural", {"tag1"}) == "things"
        assert dictionary.get("singular", {"tag2"}) == "hexagon"
        assert dictionary.get("plural", {}, {"tag1"}) == "hexagons"


if __name__ == "__main__":
    test_tag_requirement()
