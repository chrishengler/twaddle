from parser.rant_object import *
from collections import deque
from lexer.rant_token import *
import lexer.rant_lexer as RantLexer
import parser.rant_parser as RantParser


def get_parse_result(sentence: str) -> deque[RantObject]:
    return RantParser.parse(RantLexer.lex(sentence))
    


def test_parse_text():
    parser_output = get_parse_result("hello") 
    assert len(parser_output) == 1
    assert parser_output[0].type == RantObjectType.TEXT
    assert parser_output[0].text == "hello"


def test_parse_simple_lookup():
    parse_result = get_parse_result("<whatever>")
    assert len(parse_result) == 1
    lookup: RantLookupObject = parse_result[0]
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "whatever"


def test_parse_complex_lookup():
    parse_result = get_parse_result("<dictionary.form-category>")
    assert len(parse_result) == 1
    lookup: RantLookupObject = parse_result[0]
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.form == "form"
    assert lookup.category == "category"


def test_parse_function():
    lex_result = get_parse_result("[function:arg1;arg2]")
    assert len(lex_result) == 1
    assert isinstance(lex_result[0], RantFunctionObject)
    func: RantFunctionObject = lex_result[0]
    assert func.func == "function"
    assert len(func.args) == 2
    assert func.args[0] == "arg1"
    assert func.args[1] == "arg2"

def test_parse_choice():
    parser_output = get_parse_result("{this|that}")
    assert len(parser_output) == 1
    assert isinstance(parser_output[0], RantBlockObject)
    choice_result: RantBlockObject = parser_output[0]
    assert choice_result.type == RantObjectType.BLOCK
    assert len(choice_result.choices) == 2
    for choice in choice_result.choices:
        assert len(choice) == 1
        assert isinstance(choice[0], RantTextObject)
    assert choice_result.choices[0][0].text == "this"
    assert choice_result.choices[1][0].text == "that"


if __name__ == "__main__":
    test_parse_function()
