# Twaddle Runner

The TwaddleRunner class is the intended interface by which users interact with Twaddle.

It is imported from `twaddle.runner` and accepts two arguments on instantiation:

`runner = TwaddleRunner(<path>, <persistent>)`

`path` is a mandatory string argument. It specifies the path containing the dictionary files
to be loaded.

`persistent` is an optional bool argument. It defaults to `False` if not specified. If 
`persistent` is set to `True`, the TwaddleRunner will operate in [persistent mode](persistent.md).

