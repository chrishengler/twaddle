class TwaddleException(Exception):
    """Base class for others"""

    def __init__(self, message: str):
        super().__init__(message)


class TwaddleLexerException(TwaddleException):
    """Thrown when lexer gets confused"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class TwaddleParserException(TwaddleException):
    """Thrown when parser gets confused"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class TwaddleInterpreterException(TwaddleException):
    """Thrown when interpreter gets confused"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class TwaddleLookupException(TwaddleException):
    """Thrown when lookup fails"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)
