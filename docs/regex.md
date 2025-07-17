# Regex

If you don't know what regular expressions are, this is probably best
ignored for the sake of your own sanity. 

If you do know what regular expressions are, then I warn you that this 
implementation follows that of Rant v3. It is truly hideous and the same
advice may still apply regarding sanity.

Improved syntax may be available in a later version.

You can use regular expressions (regex) to manipulate Twaddle output. The syntax is 
similar to other Twaddle [functions](functions.md), but the regex itself 
(demarcated with a double slash `//` marking its beginning and end) takes 
the place of the function name. 

Two arguments are accepted: the text to run the regex on, and the text to be
used in place of any matches:

`[//<regex>//:<text>;<replacement>]`

`regex` is the regex to be run,

`text` is the text over which the regex should run

`replacement` is the text which should be used as a replacement for each regex match

So a very simple use of a regular expression in Twaddle looks like:

`[//\ss//:a silly snake was in the sand; sss]`

which produces the output:

 `a sssilly sssnake was in the sssand`

All standard Twaddle sentence features are available within the text.
For example:

`[//^\w//:<noun>;XXX]`

will replace the first character of the line with `XXX`, giving a result of
perhaps `XXXotorbike`

Similarly, Twaddle sentence features can be used within the replacement:

`[//[124]//:1 2 3 4 5;<noun.plural>]`

will replace the characters 1, 2, and 4 with a randomly chosen plural noun, 
giving results like:

`air fresheners people 3 warehouses 5`

Additionally, the `match` [function](functions.md) can be used within the
replacement text to insert the sequence which was matched, for example:

`[//[aeiou]+//:double vowel sequences;[match][match]]`

produces:

`dououblee vooweel seequeuencees`

## Regex flavour

The regex implementation is provided by the re module from the Python
standard library. Consult the 
[module documentation](https://docs.python.org/3/library/re.html#module-re)
for more on the syntax. 


