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

Full installation instructions will be provided at a later date, but if you've worked with Python you should have no
trouble getting the module set up.

To actually use it, create a TwaddleRunner object, passing it the location of the folder containing the dictionary files you 
wish to use. Then give your sentences to its `run_sentence` method. For an extremely simple example, see the 
`__main__.py` file, which takes sentences as console input and prints the result:

```
import sys

from runner import TwaddleRunner


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

