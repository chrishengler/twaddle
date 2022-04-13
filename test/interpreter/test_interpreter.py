import interpreter.interpreter as Interpreter
import parser.rant_parser as Parser
import lexer.rant_lexer as Lexer


def get_interpreter_output(sentence):
    return Interpreter.interpret(Parser.parse(Lexer.lex(sentence)))


def test_plain_text():
    hello_world = "hello, world"
    result = get_interpreter_output(hello_world)
    assert result == hello_world


def test_text_with_special_characters():
    special_characters = "|-;::/:!.="
    result = get_interpreter_output(special_characters)
    assert result == special_characters

def test_choice():
    result = get_interpreter_output("{a|b}")

    assert result == 'a' or result == 'b'


if __name__ == "__main__":
    test_text_with_special_characters()
