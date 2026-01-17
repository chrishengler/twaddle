# Twaddle Introduction

Twaddle is a python package for templated text generation.  It originated
as a reimplementation of a subset of [Rant v3](https://github.com/TheBerkin/rant3).
A number of new features have since been added, though it remains 
backwards compatible with the targeted Rant subset.


## OK, so what does that mean?

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

- [Abbreviations](abbreviations.md)
- [Branching templates](branching.md)
- [Capitalization schemes](capitalization.md)
- [Clipboards](clipboard.md)
- [Functions](functions.md)
- [Loops](loops.md)
- [Patterns](patterns.md)
- [Regular expressions](regex.md)
- [Synchronizers](synchronizers.md)

## How do I get started?

Below is a quick guide as a memory aid for those already familiar with 
how Twaddle works.  For full installation and usage documentation, see 
[using Twaddle](using.md).

### Quick guide

You can install Twaddle via pip

`pip install twaddle`

You can then import the TwaddleRunner class:

`from twaddle.runner import TwaddleRunner`

Instantiate it with the path to your dictionaries and choice of 
whether to use [persistent mode](persistent.md):

`runner = TwaddleRunner(<path_to_dictionaries>, persistent=<True/False>)`

And you're ready to start feeding it your sentences:

`runner.run_sentence(<your_twaddle_sentence_here>)`
