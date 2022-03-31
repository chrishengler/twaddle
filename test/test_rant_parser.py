from rant_object import *
import rant_lexer as RantLexer
import rant_parser as RantParser


def test_parse_text():
    rt = RantToken(RantTokenType.PLAIN_TEXT, "hello")
    parser_input = [rt]
    parser_output = RantParser.parse(parser_input)
    assert len(parser_output) == 1
    assert parser_output[0].type == RantObjectType.TEXT
    assert parser_output[0].text == "hello"


def test_parse_simple_lookup():
    lex_result = RantLexer.lex("<whatever>")
    parser_output = RantParser.parse(lex_result)
    assert len(parser_output) == 1
    assert isinstance(parser_output[0], RantLookupObject)
    lookup: RantLookupObject = parser_output[0]
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "whatever"
    assert lookup.form == ""
    assert lookup.category == ""
    assert lookup.label == ""


def test_parse_complex_lookup():
    lex_result = RantLexer.lex("<dictionary.form-category>")
    parser_output = RantParser.parse(lex_result)
    assert len(parser_output) == 1
    assert isinstance(parser_output[0], RantLookupObject)
    lookup: RantLookupObject = parser_output[0]
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.form == "form"
    assert lookup.category == "category"
    assert lookup.label == ""


if __name__ == "__main__":
    test_parse_complex_lookup()
