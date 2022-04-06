import rant_lexer as RantLexer
import rant_lookup_factory as LookupFactory
from rant_object import RantLookupObject, RantObjectType
from rant_exceptions import RantParserException


def test_parse_simple_lookup():
    lex_result = RantLexer.lex("<whatever>")
    lookup = LookupFactory.build(lex_result)
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "whatever"


def test_parse_complex_lookup():
    lex_result = RantLexer.lex("<dictionary.form-category>")
    lookup = LookupFactory.build(lex_result)
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.form == "form"
    assert lookup.category == "category"


def test_parse_lookup_with_label():
    lex_result = RantLexer.lex("<dictionary::=label>")
    lookup = LookupFactory.build(lex_result)
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.labels == [("label", True)]


def test_parse_lookup_with_negative_label():
    lex_result = RantLexer.lex("<dictionary::!=label>")
    lookup = LookupFactory.build(lex_result)
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.labels == [("label", False)]


def test_parse_multiple_labels():
    lex_result = RantLexer.lex("<dictionary::!=label1::!=label2>")
    lookup = LookupFactory.build(lex_result)
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.labels == [("label1", False), ("label2", False)]
