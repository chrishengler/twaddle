from collections import deque
from types import WrapperDescriptorType
from parser.rant_compiler import CompilerContextStack, CompilerContext, RantCompiler
from parser.rant_object import *
from rant_exceptions import RantParserException
from lexer.rant_token import *
import lexer.rant_lexer as RantLexer
from parser.rant_compiler import RantCompiler
import pytest

compiler = RantCompiler()

def get_compile_result(sentence: str) -> RantRootObject:
    return compiler.compile(sentence).contents


def test_compiler_context_stack():
    stack = CompilerContextStack()
    assert stack.current_context() == CompilerContext.ROOT
    stack.add_context(CompilerContext.FUNCTION)
    stack.add_context(CompilerContext.BLOCK)
    assert stack.current_context() == CompilerContext.BLOCK
    stack.remove_context(CompilerContext.BLOCK)
    assert stack.current_context() == CompilerContext.FUNCTION
    with pytest.raises(RantParserException) as e_info:
        stack.remove_context(CompilerContext.BLOCK)
        assert e_info.message == "[CompilerContextStack::remove_context] tried to remove BLOCK but current context is FUNCTION"


def test_parse_text():
    result = get_compile_result("hello")
    assert len(result) == 1
    assert result[0].type == RantObjectType.TEXT
    assert result[0].text == "hello"


def test_parse_simple_lookup():
    result = get_compile_result("<whatever>")
    assert len(result) == 1
    lookup: RantLookupObject = result[0]
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "whatever"


def test_parse_complex_lookup():
    result = get_compile_result("<dictionary.form-category>")
    assert len(result) == 1
    lookup: RantLookupObject = result[0]
    assert lookup.type == RantObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.form == "form"
    assert lookup.category == "category"


def test_parse_function():
    lex_result = get_compile_result("[function:arg1;arg2]")
    assert len(lex_result) == 1
    assert isinstance(lex_result[0], RantFunctionObject)
    func: RantFunctionObject = lex_result[0]
    assert func.func == "function"
    assert len(func.args) == 2
    assert func.args[0][0].text == "arg1"
    assert func.args[1][0].text == "arg2"


def test_parse_choice():
    parser_output = get_compile_result("{this|that}")
    assert len(parser_output) == 1
    assert isinstance(parser_output[0], RantBlockObject)
    choice_result: RantBlockObject = parser_output[0]
    assert choice_result.type == RantObjectType.BLOCK
    assert len(choice_result.choices) == 2
    for choice in choice_result.choices:
        assert len(choice.contents) == 1
    assert choice_result.choices[0][0].text == "this"
    assert choice_result.choices[1][0].text == "that"


def test_nested_block():
    parser_output = get_compile_result("{{a|b}|{c|d}}")
    assert len(parser_output) == 1
    outer_block = parser_output[0]
    assert isinstance(outer_block, RantBlockObject)
    ab: RantBlockObject = outer_block[0][0]
    cd: RantBlockObject = outer_block[1][0]
    assert len(ab) == 2
    assert len(cd) == 2
    assert ab[0][0].text == 'a'
    assert ab[1][0].text == 'b'
    assert cd[0][0].text == 'c'
    assert cd[1][0].text == 'd'


def test_parse_choice_with_lookups():
    parser_output = get_compile_result("{this|<something.form-category>}")
    assert len(parser_output) == 1
    assert isinstance(parser_output[0], RantBlockObject)
    block: RantBlockObject = parser_output[0]
    assert isinstance(block[0][0], RantTextObject)
    assert block[0][0].text == 'this'
    assert isinstance(block[1][0], RantLookupObject)
    lookup: RantLookupObject = block[1][0]
    assert lookup.dictionary == 'something'
    assert lookup.form == 'form'
    assert lookup.category == 'category'


if __name__ == "__main__":
    test_nested_block()
