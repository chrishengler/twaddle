# Patterns

Sections of a Twaddle input can be saved for later re-use within the same
sentence (or in subsequent sentences in [persistent mode](persistent.md)).

A saved section is called a pattern, and is defined by using the 
[`save` function](functions.md#save). The `save` function requires one
mandatory argument:

`[save:<name>]{<pattern>}`

`name` is the name under which the pattern will be saved. It is an error
to use the save function without specifying a name.

The `save` function is a [block function](block_functions.md), and the 
saved pattern consists of the entirety of the next block to be opened. 

## Edge-Cases and Restrictions 

In principle patterns can contain, and be saved and loaded within, any 
Twaddle features, including other patterns. Patterns cannot, however, 
contain themselves recursively. A pattern is saved at the end of the 
block defining it, and cannot be loaded until the block is closed.

The pattern is not evaluated before saving, so patterns containing
[lookups](lookups.md) or [branching](branching.md) may produce different
output (still conforming to the pattern) when loaded.

If the `save` functions is called multiple times without opening a block
to define a pattern, the next block will be saved under the name specified
in the most recent `save` call. The previous calls are ignored.

Note that while it is possible to save a pattern at any point in a Twaddle
sentence, patterns defined within [branching paths](branching.md) will 
only be saved if the path defining them is chosen.

## Examples

```
> [save:a]{hello} [load:a]
hello hello

> [save:a]{hello} [reverse]{[load:a]}
hello olleh

> [save:a]{the <adj> <noun> <verb.ed>!} [load:a] [case:upper][load:a]
the clear jug needed! the official rhino plunged! THE HAPPY PYRAMID WEDGED!

> [save:a]{a [save:b]{nested} example}, the [load:b] pattern can still be used afterwards
a nested example, the nested pattern can still be used afterwards
```