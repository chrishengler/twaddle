# Boolean Predicates and While Loops

This page documents Twaddle's boolean logic functions and while loop construct.
Boolean functions evaluate conditions and return either `"1"` (true) or `"0"` 
(false). They are designed to work seamlessly with [while loops](boolean_predicates.md#while-loops),
but can also be used standalone within regular Twaddle sentences.

## Boolean Conversion

Many of the boolean functions accept arguments and convert them to boolean 
values using the following rules:

- **Numeric values**: if a string can be parsed as a number (e.g. `"5"`, `"-3"`, 
`"2.5"`), it is considered **true** if and only if the numeric value is **greater 
than zero**. Zero and negative numbers are **false**.
- **Non-numeric strings**: a string that cannot be parsed as a number is considered 
**true** if it is **non-empty**, and **false** if it is **empty**. Whitespace is 
stripped before evaluation.

Examples:
- `"5"` → true (positive number)
- `"0"` → false (zero)
- `"-3"` → false (negative number)
- `"hello"` → true (non-empty string)
- `""` → false (empty string)

## Bool Function

Evaluates the truthiness of a single argument using the bool conversion rules 
described above.

**Syntax:**
```
[bool:<value>]
```

**Arguments:**
- `value` — any string or numeric value

**Returns:** `"1"` if true, `"0"` if false

**Examples:**
```
[bool:5]          → "1"
[bool:0]          → "0"
[bool:-3]         → "0"
[bool:hello]      → "1"
[bool:]           → "0"
```

## Numeric Comparison Functions

These functions perform numeric comparisons. Both arguments **must** be parseable 
as numbers, otherwise a `TwaddleFunctionException` is raised.

### Less Than

**Syntax:**
```
[less_than:<x>;<y>]
[lt:<x>;<y>]
```

**Arguments:**
- `x` — numeric value
- `y` — numeric value

**Returns:** `"1"` if `x < y`, otherwise `"0"`

**Examples:**
```
[less_than:2;5]      → "1"
[less_than:5;2]      → "0"
[less_than:5;5]      → "0"
[less_than:-10;-5]   → "1"
```

### Greater Than

**Syntax:**
```
[greater_than:<x>;<y>]
[gt:<x>;<y>]
```

**Arguments:**
- `x` — numeric value
- `y` — numeric value

**Returns:** `"1"` if `x > y`, otherwise `"0"`

**Examples:**
```
[greater_than:5;2]      → "1"
[greater_than:2;5]      → "0"
[greater_than:5;5]      → "0"
[greater_than:-5;-10]   → "1"
```

### Equal To

Performs comparison based on whether both arguments are numeric:

- If **both** arguments are parseable as numbers, performs **numeric comparison**
- Otherwise, performs **string comparison** (case-sensitive)

**Syntax:**
```
[equal_to:<x>;<y>]
[eq:<x>;<y>]
```

**Arguments:**
- `x` — any value
- `y` — any value

**Returns:** `"1"` if equal, otherwise `"0"`

**Examples:**
```
[equal_to:5;5]           → "1"
[equal_to:5;3]           → "0"
[equal_to:hello;hello]   → "1"
[equal_to:hello;world]   → "0"
[equal_to:5;hello]       → "0"
[equal_to:5;5.000]       → "0"
```

## Logical Operators

These functions perform logical operations on their arguments, converting them 
to boolean values using the bool conversion rules.

### Logical And

**Syntax:**
```
[and:<x>;<y>]
```

**Arguments:**
- `x` — any value
- `y` — any value

**Returns:** `"1"` if both are true, otherwise `"0"`

**Examples:**
```
[and:1;1]        → "1"
[and:1;0]        → "0"
[and:5;hello]    → "1"
[and:0;5]        → "0"
```

### Logical Or

**Syntax:**
```
[or:<x>;<y>]
```

**Arguments:**
- `x` — any value
- `y` — any value

**Returns:** `"1"` if at least one is true, otherwise `"0"`

**Examples:**
```
[or:1;1]     → "1"
[or:1;0]     → "1"
[or:0;0]     → "0"
[or:0;5]     → "1"
```

### Logical Xor

**Syntax:**
```
[xor:<x>;<y>]
```

**Arguments:**
- `x` — any value
- `y` — any value

**Returns:** `"1"` if exactly one is true, otherwise `"0"`

**Examples:**
```
[xor:1;1]        → "0"
[xor:1;0]        → "1"
[xor:0;0]        → "0"
[xor:5;hello]    → "0"
[xor:0;hello]    → "1"
```

### Logical Not

**Syntax:**
```
[not:<x>]
```

**Arguments:**
- `x` — any value

**Returns:** `"1"` if false, `"0"` if true (inverts the bool conversion)

**Examples:**
```
[not:1]          → "0"
[not:0]          → "1"
[not:5]          → "0"
[not:]           → "1"
[not:hello]      → "0"
```

## While Loops

While loops repeatedly execute a block as long as a given predicate evaluates to true
or until a maximum number of iterations is reached. Twaddle is a text-templating tool
which happens to include some basic looping and boolean logic functionality, it is not
designed for extensive calculations and running while loops with complex predicates
may result in poor performance. As such, the default maximum iterations is set relatively
low: `100`. 

**Syntax:**
```
[while:<predicate>;<max_iterations>]{<block contents>}
```

**Arguments:**
- `predicate` — a boolean expression (typically using one of the boolean functions)
- `max_iterations` - _optional_ the maximum number of iterations to run. must be 
parseable as an int. Defaults to `100` if not set. 
- `block contents` — the block to repeat

**Behavior:**

1. The predicate is evaluated
2. If the result is truthy (by bool conversion rules), the block is executed once
3. Steps 1–2 repeat until the predicate is falsy or until the block has been executed
`max_iterations` times.
4. If the predicate is falsy on the first evaluation, or `max_iterations` is 0 the block is never executed


**Examples:**

Count from 1 to 5:
```
[copy:counter]{1}[while:[less_than:[paste:counter];5]]{[copy:counter]{ [add:[paste:counter];1]}}
```

Output: `1 2 3 4 5`

Repeat until a condition is met:
```
[while:[not:[eq:<country-south_america::my_country>;Brazil]]]{<country-south_america::^=my_country> }
```

Output: repeatedly prints random South American countries until the first time Brazil is chosen.

## Combining Boolean Functions

Boolean functions can be nested and combined to create complex predicates:

```
...[while:[and:[less_than:[paste:x];10];[greater_than:[copy:y];0]]]{
  ...
}
```

This loop continues while `x < 10` AND `y > 0` (note that `x` and `y` must be copied
already with some numeric value so they can be loaded and used in the `less_than` and
`greater_than` functions on the first iteration).
