from rant_exceptions import RantLookupException
from lookup.lookup import *
import pytest

lookup = LookupEntry({"singular": "thing",
                      "plural": "things",
                      "possessive": "thing's",
                      "pluralpossessive": "things'"})

def test_lookup_type():
    assert lookup["singular"] == "thing"
    assert lookup["plural"] == "things"
    assert lookup["possessive"] == "thing's"
    assert lookup["pluralpossessive"] == "things'"

def test_dictionary():
    dictionary = LookupDictionary("noun", ["singular", "plural", "possessive", "pluralpossessive"])
    dictionary.add(lookup)
    assert len(dictionary.entries) == 1
    assert dictionary.get("singular") == "thing"
    assert dictionary.get("pluralpossessive") == "things'"
    with pytest.raises(RantLookupException) as e_info:
        dictionary.get("invalid")
        assert e_info.message == "[LookupDictionary.get] dictionary 'noun' has no form 'invalid'"
