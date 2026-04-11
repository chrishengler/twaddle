import pytest

from twaddle.exceptions import TwaddleFunctionRegistryException
from twaddle.interpreter.context import TwaddleContext
from twaddle.interpreter.function_registry import (
    FunctionRegistry,
    evaluate_args,
)
from twaddle.parser.nodes import RootNode, TextNode

placeholder_context = TwaddleContext()


class FakeInterpreter:
    def evaluate(self, root: RootNode) -> str:
        return "".join(
            node.text for node in root.contents if isinstance(node, TextNode)
        )


@pytest.fixture(autouse=True)
def clean_registry():
    original_lookup = FunctionRegistry.function_lookup.copy()
    yield
    FunctionRegistry.function_lookup = original_lookup


def make_raw_args(*values: str) -> list[RootNode]:
    return [RootNode(contents=[TextNode(text=v)]) for v in values]


class TestRegistration:
    def test_register_adds_to_lookup_by_name(self):
        @FunctionRegistry.register(name="myfunc")
        def myfunc(args, context, interpreter):
            pass

        assert "myfunc" in FunctionRegistry.function_lookup

    def test_register_adds_aliases_to_lookup(self):
        @FunctionRegistry.register(name="primary", aliases=["alt1", "alt2"])
        def func(args, context, interpreter):
            pass

        assert "primary" in FunctionRegistry.function_lookup
        assert "alt1" in FunctionRegistry.function_lookup
        assert "alt2" in FunctionRegistry.function_lookup

    def test_aliases_resolve_to_same_entry(self):
        @FunctionRegistry.register(name="primary", aliases=["alt"])
        def func(args, context, interpreter):
            pass

        assert (
            FunctionRegistry.function_lookup["primary"]
            is FunctionRegistry.function_lookup["alt"]
        )

    def test_duplicate_name_raises(self):
        @FunctionRegistry.register(name="taken")
        def first(args, context, interpreter):
            pass

        with pytest.raises(TwaddleFunctionRegistryException):

            @FunctionRegistry.register(name="taken")
            def second(args, context, interpreter):
                pass

    def test_duplicate_alias_raises(self):
        @FunctionRegistry.register(name="func_a", aliases=["shared"])
        def first(args, context, interpreter):
            pass

        with pytest.raises(TwaddleFunctionRegistryException):

            @FunctionRegistry.register(name="func_b", aliases=["shared"])
            def second(args, context, interpreter):
                pass

    def test_alias_colliding_with_existing_name_raises(self):
        @FunctionRegistry.register(name="taken")
        def first(args, context, interpreter):
            pass

        with pytest.raises(TwaddleFunctionRegistryException):

            @FunctionRegistry.register(name="other", aliases=["taken"])
            def second(args, context, interpreter):
                pass

    def test_entry_stores_metadata(self):
        @FunctionRegistry.register(
            name="myfunc",
            aliases=["mf"],
            min_args=1,
            max_args=3,
            description="does a thing",
        )
        def myfunc(args, context, interpreter):
            pass

        entry = FunctionRegistry.function_lookup["myfunc"]
        assert entry.name == "myfunc"
        assert entry.aliases == ["mf"]
        assert entry.min_args == 1
        assert entry.max_args == 3
        assert entry.description == "does a thing"

    def test_register_returns_original_function(self):
        @FunctionRegistry.register(name="myfunc")
        def myfunc(args, context, interpreter):
            return "original"

        assert myfunc([], placeholder_context, None) == "original"


class TestHandle:
    def test_handle_calls_registered_function(self):
        @FunctionRegistry.register(name="echo")
        def echo(args, context, interpreter):
            return "called"

        result = FunctionRegistry.handle(
            "echo", [], placeholder_context, FakeInterpreter()
        )
        assert result == "called"

    def test_handle_passes_raw_args(self):
        raw = make_raw_args("hello")

        @FunctionRegistry.register(name="grab")
        def grab(args, context, interpreter):
            return args

        result = FunctionRegistry.handle(
            "grab", raw, placeholder_context, FakeInterpreter()
        )
        assert result is raw

    def test_handle_passes_interpreter(self):
        interp = FakeInterpreter()

        @FunctionRegistry.register(name="check")
        def check(args, context, interpreter):
            return interpreter

        result = FunctionRegistry.handle("check", [], placeholder_context, interp)
        assert result is interp

    def test_handle_via_alias(self):
        @FunctionRegistry.register(name="primary", aliases=["alt"])
        def func(args, context, interpreter):
            return "ok"

        assert (
            FunctionRegistry.handle("alt", [], placeholder_context, FakeInterpreter())
            == "ok"
        )

    def test_handle_unknown_function_returns_none(self):
        result = FunctionRegistry.handle(
            "nonexistent", [], placeholder_context, FakeInterpreter()
        )
        assert result is None


class TestEvaluateArgs:
    def test_evaluate_args_converts_raw_to_strings(self):
        @evaluate_args
        def func(args, context, interpreter):
            return args

        raw = make_raw_args("hello", "world")
        result = func(raw, placeholder_context, FakeInterpreter())
        assert result == ["hello", "world"]

    def test_evaluate_args_preserves_interpreter(self):
        interp = FakeInterpreter()

        @evaluate_args
        def func(args, context, interpreter):
            return interpreter

        result = func([], placeholder_context, interp)
        assert result is interp

    def test_registered_with_evaluate_args(self):
        @FunctionRegistry.register(name="evaled")
        @evaluate_args
        def evaled(args, context, interpreter):
            return args

        raw = make_raw_args("a", "b")
        result = FunctionRegistry.handle(
            "evaled", raw, placeholder_context, FakeInterpreter()
        )
        assert result == ["a", "b"]
