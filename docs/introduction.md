# Twaddle Introduction

Twaddle is a python package for templated text generation.  It originated
as a reimplementation of a subset of [Rant v3](https://github.com/TheBerkin/rant3),
some minor adaptations have since been made. 

In short, Twaddle takes input like:

`The <noun-person.plural> <verb.ed-transitive> \a <adj> <noun-vehicle>.`

and - using the sample dictionaries provided in this repository - produces
output like:

`The women knew a blue helicopter`
`The men flew a big motorbike`
`The people heard a red van`
`The babies knew a sad bike`

And so on. This example sentence uses some of the most fundamental features
of Twaddle:

- [Dictionary lookups](lookups.md)
- Handling of English definite article (a/an)


Some more advanced features of Twaddle include:

- Branching templates
- Capitalization schemes
- Loops


