from rant_object import *

def test_rant_text_object():
    rt = RantTextObject("hello")
    assert rt.type == RantObjectType.TEXT
    assert rt.text == "hello"


def test_rant_lookup_object():
    rl = RantLookupObject("dictionary","form")
    assert rl.type == RantObjectType.LOOKUP
    assert rl.dictionary == "dictionary"
    assert rl.form == "form"
    rl.setNext(rl)
    assert rl.next == rl 


def test_rant_choice_object():
    r1 = RantTextObject("hello")
    r2 = RantLookupObject("name")
    choices = [ r1, r2 ]
    rc = RantChoiceObject(choices)
    ro = RantObject(RantObjectType.TEXT)
    rc.setNext(ro)
    assert rc.type == RantObjectType.CHOICE
    assert len(rc.choices) == 2
    assert rc.choices[0] == r1
    assert rc.choices[1] == r2
    assert rc.next == ro


def test_rant_function_object():
    rf = RantFunctionObject("function", ["arg0","arg1"])
    assert rf.type == RantObjectType.FUNCTION
    assert rf.func == "function"
    assert len(rf.args) == 2
    assert rf.args[0] == "arg0"
    assert rf.args[1] == "arg1"
