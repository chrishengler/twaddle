# Twaddle Introduction

Twaddle is a python package for templated text generation.  It originated
as a reimplementation of a subset of [Rant v3](https://github.com/TheBerkin/rant3),
some minor adaptations have since been made. 

For those with basic familiarity: see the [basics](basics.md).

In short, Twaddle takes input like:

`The <noun-person.plural> <verb.ed-transitive> \a <adj> <noun-vehicle>.`

and - using the sample dictionaries provided in this repository - produces
output like:

`The women knew a blue helicopter`
`The men flew a big motorbike`
`The people heard a red van`
`The babies knew an old bike`

And so on. This example sentence relies on some of the most fundamental
features of Twaddle:

- [Dictionaries](dictionaries.md)
- [Lookups](lookups.md)
- [Handling of English indefinite articles (a/an)](indefinite_articles.md)

Some more advanced features of Twaddle include:

- [Capitalization schemes](capitalization.md)
- [Branching templates](branching.md)
- [Synchronizers](synchronizers.md)
- [Functions](functions.md)
- [Loops](loops.md)
- [Regular expressions](regex.md)
