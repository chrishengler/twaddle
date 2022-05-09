from types import MemberDescriptorType


class RantException(Exception):
    """Base class for others"""

    def __init__(self, message: str):
        super().__init__(message)


class RantLexerException(RantException):
    """Thrown when lexer gets confused"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class RantParserException(RantException):
    """Thrown when parser gets confused"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class RantInterpreterException(RantException):
    """Thrown when interpreter gets confused"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class RantLookupException(RantException):
    """Thrown when lookup fails"""

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)
