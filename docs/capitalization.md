# Capitalization schemes

Twaddle can automatically provide capitalization for sentences, according to
a variety of strategies. This is applied with the case function:

`[case:<strategy>]`

## Strategies

The available strategies are:

`none`: capitalization is retained from the input sentence/dictionary entries

`upper`: puts all letters in upper case

`lower`: puts all letters in lower case

`sentence`: capitalizes letters beginning a sentence (see below for details), 
everything else in lower case

`title`: capitalizes letters beginning a word, everything else in lower case

The capitalization strategy affects the entire sentence from the point
it is applied, it is not restricted by e.g. [blocks](blocks.md). To 
cancel the effect of a capitalization strategy, apply `[case:none]`.

### Sentence case

For the sentence case strategy, the beginning of a sentence is defined as
either the first character output by the Twaddle sentence, or any character
which, ignoring whitespace, is immediately preceded by `.`, `!`, or `?`.

The English first person pronoun `I` will also be placed in upper case 
whenever it appears as a complete word while the sentence case strategy
is activated.

## Persistent mode

Even in persistent mode, capitalization strategies affect only the sentence
being run. To retain their effect for subsequent sentences, they must be
applied again at the beginning of each sentence.