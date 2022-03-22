class RantException(Exception):
    """Base class for others"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RantLexerException(RantException):
    """Thrown when lexer gets confused"""

    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(self.message)