import rant_lexer as RantLexer
import rant_lookup_factory as LookupFactory
from rant_object import RantLookupObject, RantObjectType
from rant_exceptions import RantParserException


def test_parse_simple_lookup():
    lex_result = RantLexer.lex("<whatever>")
    lookup = LookupFactory.build(lex_result)
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "whatever"
    assert lookup.form == ""
    assert lookup.category == ""
    assert lookup.label == ""


def test_parse_complex_lookup():
    lex_result = RantLexer.lex("<dictionary.form-category>")
    lookup = LookupFactory.build(lex_result)
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.form == "form"
    assert lookup.category == "category"
    assert lookup.label == ""


