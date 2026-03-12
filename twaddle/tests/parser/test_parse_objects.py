from twaddle.parser.nodes import (
    BlockNode,
    FunctionNode,
    LookupNode,
    TextNode,
)


def test_rant_text_object():
    rt = TextNode("hello")
    assert isinstance(rt, TextNode)
    assert rt.text == "hello"


def test_rant_lookup_object():
    rl = LookupNode("dictionary", "form")
    assert isinstance(rl, LookupNode)
    assert rl.dictionary == "dictionary"
    assert rl.form == "form"


def test_rant_choice_object():
    r1 = TextNode("hello")
    r2 = LookupNode("name")
    choices = (r1, r2)
    rc = BlockNode(choices)
    assert isinstance(rc, BlockNode)
    assert len(rc.choices) == 2
    assert rc.choices[0] == r1
    assert rc.choices[1] == r2


def test_rant_function_object():
    rf = FunctionNode("function", [TextNode("arg0"), TextNode("arg1")])
    assert isinstance(rf, FunctionNode)
    assert rf.func == "function"
    assert len(rf.args) == 2
    assert rf.args[0].text == "arg0"
    assert rf.args[1].text == "arg1"
