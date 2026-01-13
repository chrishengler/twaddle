# Lookups

Lookups are placeholders in a Twaddle sentence which are replaced in the
output by words defined in the loaded [dictionaries](dictionaries.md).

In this documentation, the `noun.dic` sample dictionary from this repository
is used as for illustrative examples. 

A Lookup begins and ends with angle brackets, containing the Lookup arguments.
The only mandatory argument is the dictionary name. This must be the first
argument. A simple Lookup referencing the `noun` dictionary looks like:

`<noun>`

This may be sufficient in simple use cases, but for more complex sentences 
it will be necessary to provide additional arguments.

## Specifying form

Each dictionary provides one or more forms for each term within it. Whichever
form is defined first in the list is the default, and that form is returned 
from a simple Lookup. To retrieve other forms, the form name must be specified.

The syntax for this is to place a `.` after the dictionary name, e.g. to 
retrieve a plural noun from the sample noun dictionary:

`<noun.plural>`

## Specifying class

Dictionaries may organise their entries into classes. A Lookup specifies one
or more classes by adding a dash `-` and then the class name. In this case, the
Lookup will only return terms matching all of the specified classes. For example, using the sample noun dictionary, the Lookup:

`<noun-building>` 

will only return terms defined with the class `building`. The Lookup

`<noun-retail>` 

will return only terms defined with the class `retail` (perhaps `store`, perhaps `ice cream van`), but the Lookup

`<noun-building-retail>`

will return only terms defined with both categories - in this case, `store`
would be a possible result, but `ice cream van` would not, as that is not
a part of the `building` class.

Classes may also be excluded, by placing an excalamation mark before them:

`<noun-building-!retail>`

will return only terms which are part of the `building` class but are not part
of the `retail` class. The negation applies only to the class it is written 
with. Just as multiple classes can be required, multiple classes may also be negated.

### Order

Class requirements (whether positive or negative) in a Lookup may be specified
in any order. There is no difference between, for example:

`<noun-building-!retail>` 

and

`<noun-!retail-building>`

## Labels

A Lookup can be given a Label, allowing for reuse (or avoidance) later in a
sentence. The simplest use case is to reuse a word, as in:

`You call that \a <noun::=a>? THIS is \a <noun::=a>!`

Here the Label 'a' has been applied to both uses of noun, which will therefore
always return the same word. You may get a result like:

`You call that a paperweight? THIS is a paperweight!`

or 

`You call that an ice cream van? THIS is an ice cream van!`,

but you will never get

`You call that a paperweight? THIS is an ice cream van!`

The Label section of a Lookup begins with a double colon

`::`

followed by `=` (a Positive Label), `!=` (a Negative Label), or `^=` (force 
definition, which overwrites the previous assignment if the label already existed) 
then the tag name. 

Each label is scoped to its own dictionary. The same name may be reused
as a label for multiple dictionaries, entirely independently.

### Lifespan

In [persistent mode](persistent.md), labels exist from their first
definition (as a positive label) until they are cleared. Clearing
may occur by including [the `clear` function](functions.md#clear)
in a Twaddle sentence or by the `clear` method on the TwaddleRunner.

In non-persistent mode, labels exist from their first definition 
(as a positive label) until the end of the sentence, or until the
`clear` function is used within the sentence. 

### Positive Label

Applying positive Label to a Lookup on our noun dictionary will look like this:

`<noun::=tagname>`

Using this multiple times within a sentence will ensure that each usage returns
the same word. Form arguments can still be provided separately to 
each Lookup using the Label, for example:

`I'm sick of these <noun-vehicle.plural::=a>, I hope I never see another <noun::=a>`

Class arguments will only be interpreted on the first definition of the Label.

Only one positive definition can be applied in a given lookup. If more than one
positive label is applied in a lookup, only the last one to be defined is applied:

`<noun::=a::=b>` is equivalent to `<noun::=b>`, and will leave the label `a` undefined 
unless it has previously been used.

### Negative Label

Negative Labels can be applied to ensure the returned value is distinct from
the Lookup result of any previously defined Label. For example:

`I asked for \a <noun::=a>, not \a <noun::!=a>!`

may return 

`I asked for a helicopter, not an air freshener`

or

`I asked for a baby, not a factory`

but never

`I asked for a warehouse, not a warehouse`

Negative labels will only take effect if the label has already been defined
earlier in the sentence. They work on a "best-effort" basis: if there are no 
valid results for the Lookup respecting the Negative Label, it will be ignored.

### Force Definition

If a label has already been assigned (used as a positive label), it can be updated
if necessary. To force a redefinition, use the `::^=` syntax:

`<noun-vehicle::=a> <noun::=a> <noun-shape::^=a> <noun::=a>`

redefines the label `a` after its first two uses and may produce something like

`ambulance ambulance hexagon hexagon` 

A force definition can be combined with other labels, including its own preexisting
assignment:

`<noun-vehicle::=a> <noun::=a> <noun-vehicle::^=a::!=a> <noun::=a>`

may produce `car car bike bike`, but never `car car car car` as the combination of
force definition with a negative label enforces that the lookup will not match the
label's previous assignment.

A force definition may also be applied to multiple labels in the same lookup:

`<noun-vehicle::=a> <noun::=a::^=b::^=c>`

will force labels `b` and `c` to refer to the same lookup result as label `a`.


### Definition

A label can only be defined as a positive label. A negative label where that
label name has not yet been defined is ignored. In some cases it may be desirable
to avoid matching a word earlier than the sentence


## Combining Forms, Classes, and Labels

The only ordering restriction in a Lookup is that the dictionary name must
come first. Classes, forms, and Labels may be specified in any order after
the dictionary name. Some of the below Lookups are more readable than others,
but all will be processed identically.

```
<noun.plural-vehicle-!retail::=a>
<noun-vehicle-!retail.plural::a>
<noun-!retail.plural::=a-vehicle>
<noun::=a-!retail.plural-vehicle>
```
