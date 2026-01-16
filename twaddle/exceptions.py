class TwaddleException(Exception):
    """Base class for others"""

    def __init__(self, message: str):
        super().__init__(message)


class TwaddleLexerException(TwaddleException):
    """Thrown when lexer gets confused"""

    def __init__(self, message: str):
        super().__init__(message)


class TwaddleParserException(TwaddleException):
    """Thrown when parser gets confused"""

    def __init__(self, message: str):
        super().__init__(message)


class TwaddleInterpreterException(TwaddleException):
    """Thrown when interpreter gets confused"""

    def __init__(self, message: str):
        super().__init__(message)


class TwaddleLookupException(TwaddleException):
    """Thrown when lookup fails"""

    def __init__(self, message: str):
        super().__init__(message)


class TwaddleDictionaryException(TwaddleException):
    """Thrown when dictionary file is invalid"""

    def __init__(self, message: str):
        super().__init__(message)


class TwaddleFunctionException(TwaddleException):
    """Thrown when a function is invalid"""

    def __init__(self, message: str):
        super().__init__(message)
