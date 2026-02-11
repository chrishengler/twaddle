# Error Messages and Syntax Reference

Twaddle uses the [Lark parser library](https://lark-parser.readthedocs.io/en/latest/index.html)
for parsing and takes adventage of its abilities to produce clear error
messages where possible. When Twaddle encounters invalid input, it will 
generally report an error message indicating what went wrong and where. 
This page explains the terminology used in these error messages.

## Understanding Error Messages

A typical error message looks like this:

```
Unclosed block - missing '}'
{a|b
   ^
```

The first line describes the problem, and the second line shows where in
your input the error was detected. A `^` below points to the exact position.

## Syntax Elements

Twaddle's syntax is built from several types of elements. When an error
occurs, Twaddle will often tell you what it expected to find. Here's what
each term means:

### Brackets and Delimiters

| Term | Character | Used For |
|------|-----------|----------|
| `'<'` | `<` | Opening a [lookup](lookups.md) |
| `'>'` | `>` | Closing a [lookup](lookups.md) |
| `'{'` | `{` | Opening a [block](blocks.md) |
| `'}'` | `}` | Closing a [block](blocks.md) |
| `'['` | `[` | Opening a [function](functions.md) |
| `']'` | `]` | Closing a [function](functions.md) |

To use brackets or delimiters in their raw form, they must be 
[escaped](#escape-sequences).

### Separators and Operators

| Term | Character | Used For |
|------|-----------|----------|
| `'\|'` | `\|` | Separating choices in a [block](blocks.md) |
| `';'` | `;` | Separating arguments in a [function](functions.md) |
| `':'` | `:` | Separating function name from arguments |
| `'.'` | `.` | Specifying a form in a [lookup](lookups.md) |
| `'-'` | `-` | Specifying a tag in a [lookup](lookups.md) |
| `'/'` | `/` | Used in [regex](regex.md) patterns |

These characters carry special meaning in their particular contexts, but can
be used unescaped where that special meaning is not relevant (e.g. the pipe character 
`|` may be used directly anywhere outside of a block, a semicolon `;` does not need to be 
escaped outside of function arguments, etc).

### Content Elements

| Term | Meaning | Valid Characters |
|------|---------|------------------|
| text | Regular text content | Any character except `< > { } [ ] \| \ ; /` |
| identifier | A name (dictionary, function, tag, or label) | Any character except whitespace, `! < > { } [ ] / \| \ : . -` |

The key difference is that **text** can include whitespace and punctuation like `.`, `-`,
`:`, and `!`, while **identifiers** cannot. Identifiers are used where
Twaddle needs to recognise a specific name, such as:

- Dictionary names in lookups: `<noun>`, `<verb>`
- Function names: `[rep:3]`, `[sync:name;locked]`
- Tag names: `<noun-animal>`, `<verb-transitive>`
- Label names: `<noun::=myLabel>`

### Escape Sequences

Escape sequences allow you to include special characters in your text.
They start with a backslash `\` followed by one of these characters:

| Sequence | Result |
|----------|--------|
| `\a` | Lowercase indefinite article (a/an) |
| `\A` | Uppercase indefinite article (A/An) |
| `\d` | Random digit (0-9) |
| `\n` | Newline |
| `\t` | Tab |
| `\s` | Space |
| `\\` | Literal backslash `\` |
| `\;` | Literal semicolon (useful inside function arguments) |
| `\:` | Literal colon |
| `\<` | Literal less-than symbol `<` |
| `\>` | Literal greater-than symbol `>` |
| `\{` | Literal opening curly bracket `{` |
| `\}` | Literal closing curly bracket `}` |
| `\[` | Literal opening square bracket `[` |
| `\]` | Literal closing square bracket `]` |
| `\\|` | Literal pipe character `\|` |

Only the characters listed above can follow a backslash. Using `\` with
any other character will result in an error.

## Common Errors

### Unclosed block - missing '}'

You opened a block with `{` but didn't close it with `}`.

```
{hello|world
```

Fix: Add the closing `}`:
```
{hello|world}
```

### Unclosed function - missing ']'

You opened a function with `[` but didn't close it with `]`.

```
[rep:3
```

Fix: Add the closing `]`:
```
[rep:3]
```

### Unclosed lookup - missing '>'

You opened a lookup with `<` but didn't close it with `>`.

```
<noun
```

Fix: Add the closing `>`:
```
<noun>
```

### Unexpected end of input

Twaddle reached the end of your input while still expecting more content.
This usually means something wasn't closed properly. Check that all your
brackets are balanced.

### Unexpected character

A character appeared where it wasn't valid. This most commonly applies to 
delimiters like `{`, `}`, `[`, `]`, `<`, `>` appear in places
where they have syntactic meaning. Use [escape sequences](#escape-sequences)
if you need these characters as literal text.
