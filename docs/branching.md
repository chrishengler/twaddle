# Branching templates

A Twaddle [block](blocks.md) can have multiple paths.
A pipe character (`|`) is used to
separate the paths. So the input:

`I like {cats|dogs}`

Will produce as output either 

`I like cats`

or

`I like dogs`

Each path has an equal probability of being chosen.

## Within Branches

As with blocks, there are no special restrictions on the content of 
branches. They can contain [Lookups](lookups.md):

`I like {<adj> <noun.plural>|<verb.ing>}`

producing, e.g. `I like big desks` or `I like flying`.

They can contain formatting commands:

`I like {[case:upper]capitals|[case:lower]TINY LETTERS}`

producing `I like CAPITALS` or `I like tiny letters`. 

They can be used recursively:

`I can be \a {<noun>|{<adj> <noun>|<verb.er>}}`

The equal probability applies at each level of nesting, so the example above
has a 50% chance of producing a sentence like

`I can be an air freshener`

a 25% chance of producing a sentence like

`I can be a happy motorbike`

and a 25% chance of producing a sentence like

`I can be a swimmer`