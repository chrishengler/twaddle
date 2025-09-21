# Strict mode

In some cases it may not be possible to fulfil all conditions requested
within a Twaddle sentence. Consider, for example, the sentence:

`<noun-shape::=a> <noun-shape::=b::!=a> <noun-shape::!=a::!=b>`

This output requests three entries from the `noun` dictionary,
each with the `shape` class, and each different from any previously
selected. If the loaded `noun` dictionary only has two entries with
the shape class, this cannot be fulfilled.

Twaddle generally behaves pragmatically and makes a best effort to print
_something_. For example, if a [lookup](lookups.md) specifies classes which
don't exist (or combinations of classes with no matching entries), the 
classes are ignored and a word is chosen from the entire dictionary. If
[negative labels](lookups.md#negative-label) are applied which haven't yet
been defined or which rule out all valid entries, again a word is chosen from
the entire dictionary. 

A TwaddleRunner in strict mode does not make these pragmatic attempts to 
print _something_, but instead raises an exception (derived from the
`TwaddleException` class) when encountering unfulfillable requirements.
