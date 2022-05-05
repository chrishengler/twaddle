from enum import Enum, auto
from lexer.rant_token import *
from .rant_object import *
from rant_exceptions import RantParserException
from collections import deque


class CompilerContext(Enum):
    ROOT = auto()
    FUNCTION = auto()
    LOOKUP = auto()
    BLOCK = auto()


class CompilerContextStack:
    def __init__(self):
        self.stack = deque[CompilerContext]()
        self.stack.append(CompilerContext.ROOT)

    def current_context(self):
        return self.stack[-1]

    def add_context(self, context: CompilerContext):
        self.stack.append(context)

    def remove_context(self, context: CompilerContext):
        if self.stack[-1] is not context:
            raise RantParserException(f"[CompilerContextStack::remove_context] tried to remove {context.name} but current context is {self.stack[-1].name}")
        self.stack.pop()

class RantCompiler:
    def __init__(self):
        self.context = CompilerContextStack()
