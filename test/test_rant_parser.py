from rant_object import *
import rant_parser

def test_parse_text():
    rt = RantTextObject("hello")
    parser_input = [rt]
    parser_output = rant_parser.parse(parser_input)
    assert len(parser_output) == 1
    assert parser_output[0].type == RantObjectType.TEXT
    assert parser_output[0].text == "hello"


if __name__ == "__main__":
    test_parse_text()
