# Basics

## What is Twaddle?
Twaddle implements a limited subset of [Rant v3](https://github.com/TheBerkin/rant3).

Initial targeted features are:

- dictionaries
- case functions
- blocks (including synchronizers, repeat count, and separators)
- regex application
- indefinite article choice (for English)

## How do I use Twaddle?

Twaddle can be installed from pip with

`pip install twaddle`

If you prefer, you can download the git repo directly from 

To play around with an interactive session, simply run:

`python -m twaddle <path>`

where `<path>` is replaced by the path containing the [dictionaries](dictionaries.md) you wish to load

To use Twaddle within a project of your own, you will need to create a `TwaddleRunner` object (imported
from `twaddle.runner`), passing it the location of the folder containing the dictionary files you wish to
use. Then give your sentences to its `run_sentence` method. 

For an extremely simple example, see the `__main__.py` file, which takes sentences as console input
and prints the result:

```
import readline  # noqa: F401
import sys

from twaddle.runner import TwaddleRunner


def main():
    if len(sys.argv) < 2:
        print("argument required: path to directory containing dictionary files")
        return

    path = sys.argv[1]
    twaddle = TwaddleRunner(path)

    print("hello. I'm your friendly nonsense generator. Hit Ctrl-D to exit.")

    while True:
        try:
            sentence = input(">")
            print(twaddle.run_sentence(sentence))
        except EOFError:
            quit()


if __name__ == "__main__":
    main()
```
