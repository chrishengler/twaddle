# Persistent mode

In standard usage, each [Twaddle sentence](sentences.md) is processed in isolation.
[Lookup labels](lookups.md#labels) and [synchronizers](synchronizers.md) affect 
only the sentence in which they are defined.

In some cases, it may be desired to use labels or synchronizers across multiple 
sentences. This can be enabled by instantiating the [Twaddle runner](runner.md) in
persistent mode: 

`runner = TwaddleRunner(<path_to_dictionaries>, persistent=True)`

In this case, all defined Lookup labels and synchronizers are retained and may
be re-used in subsequent sentences.