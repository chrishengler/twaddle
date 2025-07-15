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

## Available functions

### Rand

The `rand` function generates a random integer. It requires two arguments:

`[rand:<min>;<max>]`

`min` is the minimum value of the integer generated

`max` is the maximum value of the integer generated

The limits are inclusive. 

### Repeat

The repeat function, `rep`, repeats a block. See [loops](loops.md) for a
full description.

It requires one argument:

`[rep:<n>]`

`n` is the number of repetitions

### Separator

The separator function, `sep`, defines a separator between repetitions of a 
block. See [loops](loops.md) for a full description.

It requires one argument:

`[sep:<text>]`

`text` is the text to be inserted as a separator

### First

The first function, `first`, defines text to be inserted before the first
repetition of a block. See [loops](loops.md) for a full description.

It requires one argument:

`[first:<text>]`

`text` is the text to be inserted before the first repetition### First

### Last

The last function, `last`, defines text to be inserted before the last
repetition of a block. See [loops](loops.md) for a full description.

It requires one argument:

`[last:<text>]`

`text` is the text to be inserted before the last repetition

### Synchronizer

The synchronizer function, `sync`, defines a [synchronizer](synchronizers.md). 
On first use it requries two arguments:

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

The case function, `case`, sets a 
[capitalization strategy](capitalization.md). It requires one argument:

`[case:<strategy>]`

`strategy` is the capitalization strategy to use

### Match

The match function is special, and does not follow the same syntax. 
