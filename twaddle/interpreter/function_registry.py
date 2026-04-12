from functools import wraps
from itertools import chain
from typing import Callable, ClassVar, Optional

from twaddle.exceptions import TwaddleFunctionRegistryException
from twaddle.interpreter.context import TwaddleContext
from twaddle.interpreter.interpreter_decorator_protocol import (
    InterpreterDecoratorProtocol,
)
from twaddle.parser.nodes import RootNode


def evaluate_args(func):
    @wraps(func)
    def wrapper(
        args: list[RootNode],
        context: TwaddleContext,
        interpreter: InterpreterDecoratorProtocol,
        *rest,
        **kwargs,
    ):
        evaluated = [interpreter.evaluate(arg) for arg in args]
        return func(evaluated, context, interpreter, *rest, **kwargs)

    return wrapper


class FunctionEntry:
    def __init__(
        self,
        name: str,
        aliases: Optional[list[str]],
        min_args: int,
        max_args: Optional[int],
        description: str,
        handler: Callable,
    ):
        self.name = name
        self.aliases = aliases if aliases else []
        self.min_args = min_args
        self.max_args = max_args
        self.description = description
        self.handler = handler


class FunctionRegistry:
    function_lookup: ClassVar[dict[str, FunctionEntry]] = {}

    @classmethod
    def add_function_entry(cls, entry: FunctionEntry):
        all_names = list(chain([entry.name], entry.aliases))
        for name in all_names:
            if name in cls.function_lookup:
                existing = cls.function_lookup[name]
                if existing.handler is not entry.handler:
                    raise TwaddleFunctionRegistryException(
                        f"Tried to add function '{name}'({entry.handler}()) "
                        f"but a function '{name}'({existing.handler}()) is already defined"
                    )
        if entry.max_args and entry.min_args > entry.max_args:
            raise TwaddleFunctionRegistryException(
                f"Trying to add function {entry.name} with minimum args ({entry.min_args}) "
                f" greater than maximum args ({entry.max_args})"
            )
        for name in all_names:
            cls.function_lookup[name] = entry

    @classmethod
    def register(
        cls,
        name: str,
        aliases: Optional[list[str]] = None,
        min_args: int = 0,
        max_args: int = 0,
        description: str = "",
    ):
        def decorator(func):
            entry = FunctionEntry(
                name=name,
                aliases=aliases or [],
                min_args=min_args,
                max_args=max_args,
                description=description,
                handler=func,
            )
            cls.add_function_entry(entry)
            return func

        return decorator

    @classmethod
    def list_functions(cls):
        def function_info(entry: FunctionEntry) -> dict:
            return {
                "name": entry.name,
                "aliases": entry.aliases,
                "description": entry.description,
            }

        return {
            "functions": [
                function_info(entry) for entry in set(cls.function_lookup.values())
            ]
        }

    @classmethod
    def handle(
        cls,
        name: str,
        args: list[RootNode],
        context: TwaddleContext,
        interpreter: InterpreterDecoratorProtocol,
    ):
        if name in cls.function_lookup:
            handler = cls.function_lookup[name]
            num_args = len(args)
            if num_args < handler.min_args or (
                handler.max_args and num_args > handler.max_args
            ):
                errstr = f"Tried to call function {name} with {num_args} arguments. The function takes "
                if not handler.max_args:
                    errstr += f"at least {handler.min_args}"
                elif handler.max_args > handler.min_args:
                    errstr += f"{handler.min_args}-{handler.max_args}"
                else:
                    errstr += f"exactly {handler.min_args}"
                errstr += " argument(s)."
                raise TwaddleFunctionRegistryException(errstr)
            return handler.handler(args, context, interpreter)
