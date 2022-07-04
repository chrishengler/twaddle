# Basics

## What is PyRant?
PyRant implements a limited subset of [Rant v3](https://github.com/TheBerkin/rant3).

Initial targeted features are:

- dictionaries
- case functions
- blocks (including synchronizers, repeat count, and separators)
- regex application
- indefinite article choice (for English)

## How do I use PyRant

Full installation instructions will be provided at a later date, but if you've worked with python you should have no
trouble getting the module set up.

To actually use it, create a Rant object, passing it the location of the folder containing the rant dictionary files you 
wish to use. Then give your rant sentences to its `run_sentence` method. For an extremely simple example, see the 
`__main__.py` file, which takes rant sentences as console input and prints the result:

```
import sys

from pyrant.rant.rant import Rant


def main():
    if len(sys.argv) < 2:
        print("argument required: path to directory containing dictionary files")
        return

    path = sys.argv[1]
    rant = Rant(path)

    print("hello")

    while True:
        sentence = input(">")
        print(rant.run_sentence(sentence))


if __name__ == "__main__":
    main()
```

