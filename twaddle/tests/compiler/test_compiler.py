# pyright: reportInvalidStringEscapeSequence=false

import pytest

from twaddle.compiler.compiler import Compiler, CompilerContext, CompilerContextStack
from twaddle.compiler.compiler_objects import (
    BlockObject,
    FunctionObject,
    IndefiniteArticleObject,
    LookupObject,
    Object,
    ObjectType,
    RegexObject,
    TextObject,
)
from twaddle.exceptions import TwaddleParserException

standard_compiler = Compiler()
strict_compiler = Compiler(strict_mode=True)


def get_standard_compile_result(sentence: str) -> list[Object]:
    return standard_compiler.compile(sentence).contents


def get_strict_compile_result(sentence: str) -> list[Object]:
    return strict_compiler.compile(sentence).contents


def test_compiler_context_stack():
    stack = CompilerContextStack()
    assert stack.current_context() == CompilerContext.ROOT
    stack.add_context(CompilerContext.FUNCTION)
    stack.add_context(CompilerContext.BLOCK)
    assert stack.current_context() == CompilerContext.BLOCK
    stack.remove_context(CompilerContext.BLOCK)
    assert stack.current_context() == CompilerContext.FUNCTION
    with pytest.raises(TwaddleParserException) as e_info:
        stack.remove_context(CompilerContext.BLOCK)
    assert (
        str(e_info.value)
        == "[CompilerContextStack::remove_context] tried to remove BLOCK but current context is FUNCTION"
    )


def test_parse_text():
    result = get_standard_compile_result("hello")
    assert len(result) == 1
    assert result[0].type == ObjectType.TEXT
    assert isinstance(result[0], TextObject)
    assert result[0].text == "hello"


def test_parse_simple_lookup():
    result = get_standard_compile_result("<whatever>")
    assert len(result) == 1
    lookup = result[0]
    assert isinstance(lookup, LookupObject)
    assert lookup.type == ObjectType.LOOKUP
    assert lookup.dictionary == "whatever"


def test_parse_complex_lookups():
    result = get_standard_compile_result("<dictionary.form-category>")
    assert len(result) == 1
    lookup = result[0]
    assert isinstance(lookup, LookupObject)
    assert lookup.type == ObjectType.LOOKUP
    assert lookup.dictionary == "dictionary"
    assert lookup.form == "form"
    assert lookup.positive_tags == {"category"}
    result = get_standard_compile_result("<dictionary.form-!category::=a>")
    lookup = result[0]
    assert isinstance(lookup, LookupObject)
    assert len(lookup.positive_tags) == 0
    assert lookup.negative_tags == {"category"}
    assert lookup.positive_label == "a"
    result = get_standard_compile_result(
        "<dictionary-category1-category2-!category3::!=b>"
    )
    lookup = result[0]
    assert isinstance(lookup, LookupObject)
    assert lookup.positive_tags == {"category1", "category2"}
    assert lookup.negative_tags == {"category3"}
    assert not lookup.positive_label
    assert lookup.negative_labels == {"b"}
    result = get_standard_compile_result("<dictionary::^=label1::^=label2>")
    lookup = result[0]
    assert isinstance(lookup, LookupObject)
    assert lookup.redefine_labels == {"label1", "label2"}


def test_parse_function():
    lex_result = get_standard_compile_result("[function:arg1;arg2]")
    assert len(lex_result) == 1
    assert isinstance(lex_result[0], FunctionObject)
    func: FunctionObject = lex_result[0]
    assert func.func == "function"
    assert len(func.args) == 2
    arg1 = func.args[0][0]
    assert isinstance(arg1, TextObject)
    assert arg1.text == "arg1"
    arg2 = func.args[1][0]
    assert isinstance(arg2, TextObject)
    assert arg2.text == "arg2"


def test_parse_choice():
    parser_output = get_standard_compile_result("{this|that}")
    assert len(parser_output) == 1
    assert isinstance(parser_output[0], BlockObject)
    choice_result: BlockObject = parser_output[0]
    assert choice_result.type == ObjectType.BLOCK
    assert len(choice_result.choices) == 2
    for choice in choice_result.choices:
        assert len(choice.contents) == 1
    this = choice_result.choices[0][0]
    assert isinstance(this, TextObject)
    assert this.text == "this"
    that = choice_result.choices[1][0]
    assert isinstance(that, TextObject)
    assert that.text == "that"


def test_nested_block():
    parser_output = get_standard_compile_result("{{a|b}|{c|d}}")
    assert len(parser_output) == 1
    outer_block = parser_output[0]
    assert isinstance(outer_block, BlockObject)
    ab = outer_block[0][0]
    cd = outer_block[1][0]
    assert isinstance(ab, BlockObject)
    assert isinstance(cd, BlockObject)
    assert len(ab) == 2
    assert len(cd) == 2
    a = ab[0][0]
    assert isinstance(a, TextObject)
    b = ab[1][0]
    assert isinstance(b, TextObject)
    c = cd[0][0]
    assert isinstance(c, TextObject)
    d = cd[1][0]
    assert isinstance(d, TextObject)

    assert a.text == "a"
    assert b.text == "b"
    assert c.text == "c"
    assert d.text == "d"


def test_parse_choice_with_lookups():
    parser_output = get_standard_compile_result("{this|<something.form-category>}")
    assert len(parser_output) == 1
    assert isinstance(parser_output[0], BlockObject)
    block: BlockObject = parser_output[0]
    assert isinstance(block[0][0], TextObject)
    assert block[0][0].text == "this"
    assert isinstance(block[1][0], LookupObject)
    lookup: LookupObject = block[1][0]
    assert lookup.dictionary == "something"
    assert lookup.form == "form"
    assert lookup.positive_tags == {"category"}


def test_parse_indefinite_article():
    parser_output = get_standard_compile_result("\\a bow and \\a arrow")
    assert len(parser_output) == 4
    assert isinstance(parser_output[0], IndefiniteArticleObject)
    assert isinstance(parser_output[1], TextObject)
    assert parser_output[1].text == " bow and "
    assert isinstance(parser_output[2], IndefiniteArticleObject)
    assert isinstance(parser_output[3], TextObject)
    assert parser_output[3].text == " arrow"


def test_parse_escaped_characters():
    parser_output = get_standard_compile_result(r"\<angles\>")
    assert len(parser_output) == 3
    left_angle = parser_output[0]
    assert isinstance(left_angle, TextObject)
    assert left_angle.text == "<"
    angles = parser_output[1]
    assert isinstance(angles, TextObject)
    assert angles.text == "angles"
    right_angle = parser_output[2]
    assert isinstance(right_angle, TextObject)
    assert right_angle.text == ">"


def test_parse_article_in_args():
    parser_output = get_standard_compile_result(r"[rep:2][sep:\a]{<noun>}")
    separator = parser_output[1]
    assert isinstance(separator, FunctionObject)
    separator_args = separator.args
    assert isinstance(separator_args[0].contents[0], IndefiniteArticleObject)


def test_parse_simple_regex():
    parser_output = get_standard_compile_result("[//a//i:a bat;i]")
    assert len(parser_output) == 1
    rro = parser_output[0]
    assert isinstance(rro, RegexObject)
    assert rro.regex == "a"
    scope = rro.scope[0]
    assert isinstance(scope, TextObject)
    assert scope.text == "a bat"
    replacement = rro.replacement[0]
    assert isinstance(replacement, TextObject)
    assert replacement.text == "i"


# noinspection SpellCheckingInspection,PyPep8
def test_parse_complex_regex():
    parser_output = get_standard_compile_result(
        "[//^\w\w[aeiou]?//i:whatever;something]"
    )
    assert len(parser_output) == 1
    rro = parser_output[0]
    assert isinstance(rro, RegexObject)
    assert rro.regex == "^\w\w[aeiou]?"


def test_strict_mode():
    result = get_strict_compile_result("<dict-tag.form>")
    assert len(result) == 1
    lookup = result[0]
    assert isinstance(lookup, LookupObject)
    assert lookup.strict_mode


def test_raise_on_invalid_closing_brackets():
    for bracket in ["]", ">", "}"]:
        with pytest.raises(TwaddleParserException) as e_info:
            get_standard_compile_result(bracket)
        assert e_info.value is not None
        with pytest.raises(TwaddleParserException) as e_info:
            get_standard_compile_result("some text here" + bracket)
        assert e_info.value is not None


if __name__ == "__main__":
    test_parse_complex_regex()
