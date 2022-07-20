from twaddle.parser.compiler_objects import (
    BlockObject,
    FunctionObject,
    LookupObject,
    ObjectType,
    TextObject,
)


def test_rant_text_object():
    rt = TextObject("hello")
    assert rt.type == ObjectType.TEXT
    assert rt.text == "hello"


def test_rant_lookup_object():
    rl = LookupObject("dictionary", "form")
    assert rl.type == ObjectType.LOOKUP
    assert rl.dictionary == "dictionary"
    assert rl.form == "form"


def test_rant_choice_object():
    r1 = TextObject("hello")
    r2 = LookupObject("name")
    choices = [r1, r2]
    rc = BlockObject(choices)
    assert rc.type == ObjectType.BLOCK
    assert len(rc.choices) == 2
    assert rc.choices[0] == r1
    assert rc.choices[1] == r2


def test_rant_function_object():
    rf = FunctionObject("function", [TextObject("arg0"), TextObject("arg1")])
    assert rf.type == ObjectType.FUNCTION
    assert rf.func == "function"
    assert len(rf.args) == 2
    assert rf.args[0].text == "arg0"
    assert rf.args[1].text == "arg1"
