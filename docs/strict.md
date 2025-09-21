# Strict mode

In some cases it may not be possible to fulfil all conditions requested
within a Twaddle sentence. Consider, for example, the [lookup](lookups.md):

`<noun-undefined>`

If the `noun` dictionary does not contain a class `undefined`, 
this request cannot be fulfilled. 

Twaddle generally behaves pragmatically makes a best effort to print
_something_. In the example above, it will choose a random entry from the
`noun` dictionary.

A TwaddleRunner in strict mode does not make a pragmatic attempt to 
print _something_, but instead raises an exception (derived from the
`TwaddleException` class) when encountering unfulfillable requirements.

## Strict mode exception scenarios

Strict mode raises exceptions in the following scenarios, which would 
produce no error with strict mode disabled:

- Requesting or excluding a [class](lookups.md#specifying-class) 
  which does not exist in the dictionary.
- Requesting or excluding combinations of classes for which there
  are no matching entries in the dictionary.
- Applying a [negative label](lookups.md#negative-label) where that
  label has not yet been defined (if you feel a need to do this, 
  the [`hide` function](functions.md#hide) should serve your purpose).
- Applying one or more negative labels which rule out all entries
  matching the lookup's other criteria.
- Using a synchronizer on a choice block with a different number of 
  entries than the block for which it was initially defined