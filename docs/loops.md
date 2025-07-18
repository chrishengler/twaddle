# Loops

Loops may be started by applying the `rep` function to a block:

`[rep:x]{content to repeat}`

where `x` is the number of times to repeat the loop. 

`[rep:3]{ha}`

will produce:

`hahaha`

All normal Twaddle features, such as [Lookups](lookups.md) or 
[branching](branching.md) can be used within a loop.

Does nothing if `x` is 1 or less. 

## Lookups and branching within loops

Lookups and branching can be used within loops. The lookups and
branching path will be chosen anew in each iteration of the loop:

`[rep:3][sep:, ]{<noun>|<adv> <verb.ing>}`

may give:

`possibly hammering, falconer, quietly organizing`

If the loop should return the same branch each iteration, this can
be achieved by using a [locked synchronizer](synchronizers.md).
Similarly, if the lookup result should remain the same across 
iterations, this can be achieved by applying a [label](lookups.md#labels)

## Advanced loops

A number of other functions exist to extend the loop functionality, these are
placed between the `rep` function and the block to which it applies.

### Separators

A separator can be defined, which will be output between each instance of
the loop. This is done using the `sep` function:

`[rep:3][sep:, ]{more}!`

produces:

`more, more, more!`

### First

The `first` defines text which should be output before the first instance of
the loop:

`[rep:3][first:don't ]{go! }`:

producing:

`don't go! go! go!`

### Last

The `last` defines text which should be output before the last instance of
the loop:

`[rep:3][last:don't ]{go! }`:

producing:

`go! go! don't go!`
