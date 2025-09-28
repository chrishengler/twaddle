# Persistent mode

In standard usage, each [Twaddle sentence](sentences.md) is processed in isolation.
[Lookup labels](lookups.md#labels), [synchronizers](synchronizers.md), and 
[patterns](patterns.md) affect only the sentence in which they are defined.

In some cases, it may be desired to use labels or synchronizers across multiple 
sentences. This can be enabled by instantiating the [Twaddle runner](runner.md) in
persistent mode: 

`runner = TwaddleRunner(<path_to_dictionaries>, persistent=True)`

In this case, all defined persistable items are retained and may
be re-used in subsequent sentences.

The persistent items may be cleared in Python code by calling the
TwaddleRunner's `clear()` method. They may also be cleared in an interactive
session with [the `clear` function](functions.md#clear).

## Partially persistent modes

In some cases it may be desirable to retain labels for use across multiple 
sentences but not synchronizers, or vice versa. Label-only and synchronizer-only
persistent modes are also available with the `persistent_labels`,
`persistent_synchronizers`, and `persistent_patterns` options on the TwaddleRunner. 
Setting the generic `persistent` option to `True` forces all persistence kinds to
be active regardless of these parameters.

### Label-only

`runner = TwaddleRunner(<path_to_dictionaries>, persistent_labels=True)`

### Synchronizer-only

`runner = TwaddleRunner(<path_to_dictionaries>, persistent_synchronizers=True)`

### Pattern-only

`runner = TwaddleRunner(<path_to_dictionaries>, persistent_patterns=True)`