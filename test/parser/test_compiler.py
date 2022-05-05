from parser.rant_compiler import CompilerContextStack, CompilerContext
from rant_exceptions import RantParserException
import pytest

def test_compiler_context_stack():
    stack = CompilerContextStack()
    assert stack.current_context() == CompilerContext.ROOT
    stack.add_context(CompilerContext.FUNCTION)
    stack.add_context(CompilerContext.BLOCK)
    assert stack.current_context() == CompilerContext.BLOCK
    stack.remove_context(CompilerContext.BLOCK)
    assert stack.current_context() == CompilerContext.FUNCTION
    with pytest.raises(RantParserException) as e_info:
        stack.remove_context(CompilerContext.BLOCK)
        assert e_info.message == "[CompilerContextStack::remove_context] tried to remove BLOCK but current context is FUNCTION"

