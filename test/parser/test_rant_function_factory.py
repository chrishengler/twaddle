import lexer.rant_lexer as RantLexer
from parser.rant_object import RantFunctionObject, RantLookupObject, RantObjectType, RantTextObject
import parser.rant_function_factory as FunctionFactory


def test_simple_function():
    lex_result = RantLexer.lex("[c]")
    parsed_function = FunctionFactory.build(lex_result)
    assert isinstance(parsed_function, RantFunctionObject)
    assert parsed_function.func == 'c'
    assert len(parsed_function.args) == 0


def test_function_with_argument():
    lex_result = RantLexer.lex("[rep:3]")
    parsed_function = FunctionFactory.build(lex_result)
    assert isinstance(parsed_function, RantFunctionObject)
    assert parsed_function.func == 'rep'
    assert len(parsed_function.args) == 1
    assert parsed_function.args[0] == '3'


def test_function_with_many_arguments():
    lex_result = RantLexer.lex("[example:a;b;c;d;e]")
    parsed_function = FunctionFactory.build(lex_result)
    assert isinstance(parsed_function, RantFunctionObject)
    assert parsed_function.func == 'example'
    assert len(parsed_function.args) == 5
    for arg in zip(parsed_function.args, ['a','b','c','d','e']):
        assert arg[0] == arg[1]


if __name__ == "__main__":
    test_function_with_many_arguments();
