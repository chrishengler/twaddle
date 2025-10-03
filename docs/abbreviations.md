# Abbreviations

The `abbreviate` or `abbr` function creates an abbreviation from the 
words of the following block. Below is a simple example input and the
corresponding output.

```
>[abbr]{Hello, internet}!
HI!
```

## Abbreviation algorithm

The abbreviation is created by splitting the block at whitespace, and taking 
the first alphabetic character _or_ string of one-or-more numeric digits 
from each component. Any components which do not include an alphabetic 
character or string of digits do not contribute to the abbreviation.

Some illustrative examples:

```
>[abbr]{Every 24 Hours}
E24H
>[abbr]{$ABC ???4}
A4
>[abbr]{$ABC ??? Hi}
AH
>[abbr]{Hello\nInternet}
HI
```

## Arguments

The function does not require any arguments. One optional argument is
permitted:

`[abbr:<case>]`

The case argument, if provided, must have one of the following values:

- `upper`: puts the entire abbreviation into upper case
    ```
    >[abbr]{hello everyone, I'm Twaddle}
    HEIT
    ```
- `lower`: puts the entire abbreviation into lower case
    ```
    >[abbr]{hello everyone, I'm Twaddle}
    heit
    ```
- `retain`: each character retains its capitalisation from the unabbreviated text
    ```
    >[abbr]{hello everyone, I'm Twaddle}
    heIT
    ```
- `first`: only the first character is capitalised
    ```
    >[abbr]{hello everyone, I'm Twaddle}
    Heit
    ```

If no argument is provided (`[abbr]`), the default value is `upper`.

Providing any other value, including the empty string, results in a `TwaddleFunctionException`
being raised.
