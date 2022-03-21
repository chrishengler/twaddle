from enum import Enum, auto

class RantTokenType(Enum):
    LEFT_ANGLE_BRACKET = auto()
    RIGHT_ANGLE_BRACKET = auto()
    LEFT_CURLY_BRACKET = auto()
    RIGHT_CURLY_BRACKET = auto()
    LEFT_SQUARE_BRACKET = auto()
    RIGHT_SQUARE_BRACKET = auto()
    PLAIN_TEXT = auto()


class RantToken:
    def __init__(self, t: RantTokenType, val: str=""):
        self.type = t
        self.value = val

    def __eq__(self, o: object) -> bool:
        return self.type == o.type and self.value == o.value

    def __str__(self) -> str:
        return f"RantToken (type: {self.type}; value: {self.value})"
