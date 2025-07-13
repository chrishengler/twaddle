# Definite articles

The English language definite article (a/an) varies depending on the initial
sound of the following word. As it depends on sound rather than spelling, this
is not trivial to implement with complete accuracy. 

Twaddle does not claim to be perfect, but offers a 'good enough' attempt at 
automatically determining the correct form based on an algorithm described 
below.

To make use of this, write `\a` in your sentence where you want the article
to appear. To illustrate, the input:

`Give me \a <noun>`

May produce:

`Give me a desk`

or 

`Give me an air freshener`

## Algorithm

The algorithm is fundamentally built on the assumption that `an` is typically
correct when the following word begins with a vowel, and `a` when it begins
with a consonant. A number of known exceptions are considered in the form of
both full words and of common prefix strings. If the following word is the
letter `u` alone, or begins with one of the below prefixes, then `\a` resolves
to `a` despite being followed by a (written) vowel.

`uni, use, uri, urol, u., one, uvu, eul, euk, eur,`

Likewise if the entire following word is:

`f, fbi, fcc, fda, x, l, m, n, s, h`

or if the word begins with any of the following strings:

`honest, honor, hour, 8`

then `\a` resolves to `an` despite not being followed by a (written) consonant.

The algorithm is not case-sensitive.