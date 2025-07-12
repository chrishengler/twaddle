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

will return only terms which are part of the `building` class but are not part of the `retail` class. 

## Tag

A Lookup can be given a tag, allowing for reuse later in a sentence. The 
tag is defined by 
