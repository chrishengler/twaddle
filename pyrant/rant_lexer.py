from pyrant.rant_token import RantToken, RantTokenType

def lex(input_str: str) -> list[RantToken]:
    output = []

    i=0
    while i < len(input_str):
        next_char_type = _get_token_type(input_str[i])
        if next_char_type is not RantTokenType.PLAIN_TEXT:
            output.append(RantToken(next_char_type))
            i+=1
        else:
            text, length = _consume_plain_text(input_str[i:])
            output.append(RantToken(RantTokenType.PLAIN_TEXT, text))
            i+=length

    return output



def _get_token_type(input_char: str) -> RantToken:
    assert(len(input_char) != 0)
    match input_char:
        case '<': return RantTokenType.LEFT_ANGLE_BRACKET
        case '>': return RantTokenType.RIGHT_ANGLE_BRACKET
        case '{': return RantTokenType.LEFT_CURLY_BRACKET
        case '}': return RantTokenType.RIGHT_CURLY_BRACKET
        case '[': return RantTokenType.LEFT_SQUARE_BRACKET
        case ']': return RantTokenType.RIGHT_SQUARE_BRACKET
        case _: return RantTokenType.PLAIN_TEXT


def _consume_plain_text(input_str: str) -> tuple[str,int]:
    for i, char in enumerate(input_str):
        if _get_token_type(char) is not RantTokenType.PLAIN_TEXT:
            return input_str[:i], i
    return input_str, len(input_str)

