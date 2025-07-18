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

### Installation

Twaddle can be installed from pip with

`pip install twaddle`

If you have git installed on your command line, you can download the git repo directly with the command 

`git clone https://github.com/chrishengler/twaddle.git`

### Interactive Use

To play around with an interactive session, simply run:

`python -m twaddle <path>`

where `<path>` is replaced by the path containing the [dictionaries](dictionaries.md) 
you wish to load.  If you have downloaded the git repo, it contains some sample dictionaries 
in the folder `twaddle/sample_dicts`.

A wider variety of dictionaries can be obtained from the official Twaddle dictionary repository:

`git clone https://github.com/chrishengler/twaddle-dict.git`

### Using in a Project

#### Dictionaries

Projects using Twaddle require a set of dictionary files. It is anticipated that these will be 
written to suit the needs of each project, but an official dictionary is available containing a 
number of dictionary files which can be used as a starting point. The repository is provided
under the MIT license at 

https://github.com/chrishengler/twaddle-dict

#### Running Twaddle

To use Twaddle within a project of your own, you will need to [create a `TwaddleRunner` object](runner.md) 
(imported from `twaddle.runner`), passing it the location of the folder containing the dictionary files 
you wish to use. Then give your [Twaddle sentences](sentences.md) to its `run_sentence` method. 

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
