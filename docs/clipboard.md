# Clipboard

Twaddle implements a clipboard feature with the `copy` and `paste`
[functions](functions.md). This allows the evaluated result of a block
to be saved for later reuse. A block's result is copied to a named 
clipboard with the `copy` function, which takes one mandatory argument:

`[copy:<name>]{<block>}`

`name` is the name of the clipboard to which the block's result will
be copied. The clipboard name can be freely chosen (in principle even using
[lookups](lookups.md) or applying other [functions](functions.md) to
determine the actual clipboard name, although it's beyond me why anybody 
would want to do that).

The `copy` function is a [block function](block_functions.md), and the
clipboard will save the entire evaluated contents of the next block to
be opened. The result is saved to the clipboard before applying other
functions such as [reverse](functions.md#reverse) which would modify the
text. If it is desired to save the modified text, the `copy` function
should be placed in an external block.

The `paste` function loads a copied block from the clipboard. It takes
one mandatory and one optional argument:

`[paste:<name>;<fallback>]`

`name` is the name of the clipboard from which to paste.

`fallback` is the pattern to run if the clipboard does not exist.
Attempting to paste from a clipboard to which nothing has been copied
will result in an error unless the `fallback` option is provided.


## Edge-Cases and Restrictions

In principle clipboard items can contain, and be copied/pasted within,
any Twaddle features, including other clipboard items. They cannot, however,
contain themselves recursively. A clipboard item is copied at the end of the
block defining it, and cannot be pasted until the block is closed.

The pattern is evaluated before copying, so even blocks containing 
[lookups](lookups.md) and [branching](branching.md) will produce the 
same output each time. If this is not desired, use [saved patterns](patterns.md)
instead.

If the `copy` functions is called multiple times without opening a block
to define the clipboard item, the next block will be copied under the name 
specified in the most recent `copy` call. The previous calls are ignored.

Note that while it is possible to copy a block at any point in a Twaddle
sentence, blocks defined within [branching paths](branching.md) will 
only be copied if the path defining them is chosen.

## Difference from saved patterns

The clipboard may be easily confused with the [saved patterns](patterns.md)
function. The difference lies in the fact that the clipboard saves the
evaluated result of the following block, whereas patterns are saved
before evaluation and are evaluated anew each time they occur.

## Examples

```
>[copy:a]{hello} [paste:a]
hello hello

>[copy:a][reverse]{hello} [paste:a]
olleh hello

>[copy:a]{[reverse]{hello}} [paste:a]
olleh olleh

>[copy:a]{the <adj> <noun> <verb.ed>!} [paste:a] [case:upper][paste:a]
the electric buzzard strained! the electric buzzard strained! THE ELECTRIC BUZZARD STRAINED!
```