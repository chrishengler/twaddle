# Function Registry Redesign

## Problem

Functions are currently accessed via a flat dictionary mapping name to callable, with a separate `SPECIAL_FUNCTIONS` list intercepted ahead of the dictionary for bespoke handling in the interpreter. All functions receive the same three arguments (`evaluated_args`, `context`, `raw_args`) regardless of whether they use them.

## Design

Replace the dictionary and special-function interception with a single registry class. Every function — including the current "special" ones (`if`, `clear`, `load`, `paste`) — is registered the same way.

### Uniform calling convention

All handlers receive:

```python
handler(raw_args: list[RootNode], context: TwaddleContext, interpreter: Interpreter)
```

Raw args are always passed. The interpreter is always passed. Functions that don't need the interpreter simply ignore it — one unused parameter is an acceptable trade-off for a branchless, single-line dispatcher.

### Auto-evaluate decorator

Most functions want their args as evaluated strings. A decorator wraps the handler so that `raw_args` arrives pre-evaluated as `list[str]`:

```python
@auto_evaluate
def add(args: list[str], context: TwaddleContext, interpreter: Interpreter) -> str:
    ...
```

Functions that need raw args (e.g. `separator`, `first`, `last`, `if`, `while`) skip the decorator:

```python
def separator(raw_args: list[RootNode], context: TwaddleContext, interpreter: Interpreter):
    context.block_attributes.separator = raw_args[0]
```

The decorator does `[interpreter.run(a).resolve() for a in raw_args]` before calling through. The type annotation on the first parameter (`list[str]` vs `list[RootNode]`) makes each function's mode self-documenting.

### Registry entry metadata

Each registered function carries:

| Field | Type | Purpose |
|---|---|---|
| `name` | `str` | Primary name |
| `aliases` | `list[str]` | Alternative names |
| `min_args` | `int` | Minimum argument count |
| `max_args` | `int \| None` | Maximum argument count (`None` = unbounded) |
| `description` | `str` | Human-readable docstring for self-documentation API |
| `handler` | `Callable` | The function implementation |

Arg count validation moves into the registry's dispatch method, removing the repetitive checks from individual function bodies.

### Dispatcher

The interpreter's `FunctionNode` handler becomes:

```python
result = self.registry.call(func.func, func.args, self.context, self)
```

No special-function interception. No branching on function type. The registry looks up the entry, validates arg count, and calls the handler.

### Self-documentation

The registry can expose its entries for introspection — a future `[help]` or `[list]` function just iterates the registry and reads name, aliases, arg counts, and description from each entry.

## Rationale

- **Raw args as the universal currency**: the split between raw and evaluated was the root cause of the uniform-three-arg signature and the special-function interception. Passing raw always and letting functions evaluate when needed removes both problems.
- **Always pass interpreter**: the only "extra" thing a function might need is the interpreter (to evaluate args or for control flow). Gating this behind a flag saves nothing for one parameter — just pass it.
- **Decorator for evaluation**: most functions want strings. The decorator keeps that boilerplate out of ~15 function bodies without hiding what's happening.
- **No special functions**: `if`, `clear`, `load`, `paste` register the same way as everything else. The interpreter has one code path for all functions.
