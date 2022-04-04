import rant_lexer as RantLexer
import rant_block_factory as BlockFactory
from rant_object import *
from rant_exceptions import RantParserException


def test_parse_choice():
    lex_result = RantLexer.lex("{this|that}")
    choice_result = BlockFactory.build(lex_result)
    assert choice_result.type == RantObjectType.BLOCK
    assert len(choice_result.choices) == 2
    for choice in choice_result.choices:
        assert len(choice) == 1
        assert isinstance(choice[0], RantTextObject)
    assert choice_result.choices[0][0].text == "this"
    assert choice_result.choices[1][0].text == "that"
