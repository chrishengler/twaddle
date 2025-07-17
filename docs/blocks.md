# Blocks

Twaddle blocks are demarcated by curly brackets:

`This is plain text {this is a block}`

A simple block just prints its contents as if the block weren't there, 
they are not useful in isolation.

`{this is a block}`

produces

`this is a block`

## Making blocks useful

Blocks are used to contain [branching paths](branching.md), and to demarcate
which section of text should be affected by some [functions](functions.md).

### Branching

Blocks can offer multiple paths for a Twaddle sentence, one of which will
be chosen. The paths are separated by a pipe character `|`:

`I like {cats|dogs}`

prints either `I like cats` or `I like dogs`. By default the path is chosen
at random for each block encountered, but [synchronizers](synchronizers.md) 
can be used to enforce relationships between the selection across multiple 
sets of paths.

See the [branching](branching.md) documentation for a fuller description.

### Functions

Some functions operate on the text contained within a block. The `hide`
function, for example, hides the text contained within the next block
encountered:

`[hide]{in}visible text`

produces the output

`visible text`

Not all functions use blocks, see the [functions](functions.md) page
for more details.