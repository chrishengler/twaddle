# Functions 

Twaddle offers a handful of functions. Most of these are related to behaviour
in [looping](loops.md) or [branching](branching.md) and are described in more 
depth in the related documentation. 

## Syntax

Twaddle functions are enclosed within square brackets. The square brackets
contain the function name, then its arguments. 

The function name is separated from any arguments by a colon. If the 
function accepts multiple arguments, they are separated from each other
by a semicolon. So this:

`[rand:0,10]`

calls the `rand` function with two arguments: `0`, and `10`. 

### Block functions

Some functions take effect wherever they are encountered in the Twaddle sentence,
others are "block functions". Block functions apply their effect to the next
block encountered within the sentence. 

See [block functions](block_functions.md) for a fuller description.

Block functions are marked in the list below.

## Available functions

### Rand

The `rand` function generates a random integer. It requires two arguments:

`[rand:<min>;<max>]`

`min` is the minimum value of the integer generated

`max` is the maximum value of the integer generated

The limits are inclusive. 

### Reverse

The `reverse` function is a [block function](block_functions.md). 
It prints the following block in reverse:

`[reverse]{oh no, \a <noun>!}`

It takes no arguments.


### Repeat

The repeat function, `rep`, is a [block function](block_functions.md).  
It repeats the block.  See [loops](loops.md) for a full description.

It requires one argument:

`[rep:<n>]`

`n` is the number of repetitions

### Separator

The separator function, `sep`, is a [block function](block_functions.md).
It defines a separator between repetitions of a 
block. See [loops](loops.md) for a full description.

It requires one argument:

`[sep:<text>]`

`text` is the text to be inserted as a separator

### First

The first function, `first`, is a [block function](block_functions.md).
It defines text to be inserted before the first
repetition of a block. See [loops](loops.md) for a full description.

It requires one argument:

`[first:<text>]`

`text` is the text to be inserted before the first repetition### First

### Last

The last function, `last`, is a [block function](block_functions.md).
It defines text to be inserted before the last repetition of a block. 
See [loops](loops.md) for a full description.

It requires one argument:

`[last:<text>]`

`text` is the text to be inserted before the last repetition

### Synchronizer

The synchronizer function, `sync`, is a [block function](block_functions.md).
It defines a [synchronizer](synchronizers.md).  On first use it requires 
two arguments:

`[sync:<name>;<type>]`

`name` is the name of the synchronizer

`type` is the type of synchronizer

On subsequent uses, it requires one argument:

`[sync:<name>]`

`name` is the name of the synchronizer.

For backwards-compatibility `x` is supported as a synonym of `sync`, with the
same syntax, but its use is not recommended except where saving characters is
a priority.

### Case

By default the output of Twaddle retains capitalization from the input and
in the case of [lookups](lookups.md) from dictionary entries. The case 
function, `case`, changes this. It sets a 
[capitalization strategy](capitalization.md). It requires one argument:

`[case:<strategy>]`

`strategy` is the capitalization strategy to use. 

The capitalization strategy affects the entire sentence from the point
it is applied, it is not restricted by e.g. [blocks](blocks.md). To 
cancel the effect of a capitalization strategy, apply `[case:none]`.

### Regular Expressions

Regular expressions can be used to match and replace patterns within text.
The pattern takes the place of the function name, and is demarcated by a
double slash `//` at each end. Two arguments are accepted:

`[//<regex>//:<text>;<replacement>]`

`regex` is the regex to be run,

`text` is the text over which the regex should run

`replacement` is the text which should be used as a replacement for each regex match

See the [regex documentation page](regex.md) for more details.

### Match

The match function can only be used within the replacement text argument
a [regex](regex.md). It inserts the text matching the regex. It takes no arguments.

`[match]`

See the [regex documentation page](regex.md) for more details.

### Hide

The `hide` function is a [block function](block_functions.md). 
It allows for a block to be processed but excluded from the output.

### Clear

The `clear` function clears any defined [labels](lookups.md#labels) and 
[synchronizers](synchronizers.md). It takes no arguments:

`[clear]`

This function is primarily useful in [persistent mode](persistent.md), 
although it can also be used within a Twaddle sentence if desired. When
used within a sentence, any labels and synchronizers defined before the 
`clear` function is inserted will be reset from the point in the sentence
where the `clear` function is used. For example:

`<noun::=a> <noun::=a> [clear]<noun::=a> <noun::=a>`

May produce sentences like

`raisin raisin shirt shirt`
`jug jug llama llama`
`robin robin market market`