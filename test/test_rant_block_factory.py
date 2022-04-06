from collections import deque
import rant_lexer as RantLexer
import rant_block_factory as BlockFactory
from rant_object import *
from rant_exceptions import RantParserException


def test_parse_choice():
    lex_result = RantLexer.lex("{this|that}")
    print( type(lex_result))
    choice_result = BlockFactory.build(lex_result)
    assert choice_result.type == RantObjectType.BLOCK
    assert len(choice_result.choices) == 2
    for choice in choice_result.choices:
        assert len(choice) == 1
        assert isinstance(choice[0], RantTextObject)
    assert choice_result.choices[0][0].text == "this"
    assert choice_result.choices[1][0].text == "that"


def test_parse_block_with_embedded_lookup():
    lex_result = RantLexer.lex("{<lookup>}")
    result = BlockFactory.build(lex_result)
    assert result.type == RantObjectType.BLOCK
    assert len(result.choices) == 1
    assert len(result.choices[0]) == 1
    assert isinstance(result.choices[0][0], RantLookupObject)
    assert result.choices[0][0].dictionary == "lookup"


def test_parse_choice_with_embedded_lookups():
    lex_result = RantLexer.lex("{<lookup1>|<lookup2>|<lookup3>}")
    result = BlockFactory.build(lex_result)
    assert result.type == RantObjectType.BLOCK
    assert len(result.choices) == 3
    for i, choice in enumerate(result.choices, 1):
        assert len(choice) == 1
        assert isinstance(choice[0], RantLookupObject)
    assert choice[0].dictionary == ("lookup" + str(i))


if __name__ == "__main__":
    test_parse_choice()
