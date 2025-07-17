# Block functions

Block functions are a subset of Twaddle [functions](functions.md).
Rather than taking effect wherever they are encountered in the Twaddle
sentence, they set parameters for the next [block](blocks.md). This will
typically be placed immediately after the function definition. This is not
required to be the case, and the effect will still apply to the next block
even when they are separated. 

For example:

`[hide]some {secret }stuff`

prints:

`some stuff`

This is because the `hide` function hides the next block, regardless of
any gaps between the function and the block.

## Scope

The effect of the block function will apply to the next block to open,
when reading the sentence left-to-right. This occurs even if the block
function is contained within a block itself, allowing for block functions
to be set variably based on [branching paths](branching.md).