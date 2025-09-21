# Using Twaddle

## Installation

Twaddle can be installed from pip with

`pip install twaddle`

If you have git installed on your command line, you can download the git repo directly with the command 

`git clone https://github.com/chrishengler/twaddle.git`

## Interactive Use

To play around with an interactive session, simply run:

`python -m twaddle <path>`

where `<path>` is replaced by the path containing the [dictionaries](dictionaries.md) 
you wish to load.  If you have downloaded the git repo, it contains some sample dictionaries 
in the folder `twaddle/sample_dicts`.

A wider variety of dictionaries can be obtained from the official Twaddle dictionary repository:

`git clone https://github.com/chrishengler/twaddle-dict.git`

## Using in a Project

### Dictionaries

Projects using Twaddle require a set of dictionary files. It is anticipated that these will be 
written to suit the needs of each project, but an official dictionary is available containing a 
number of dictionary files which can be used as a starting point. The repository is provided
under the MIT license at 

https://github.com/chrishengler/twaddle-dict

### Running Twaddle

To use Twaddle within a project of your own, you will need to [create a `TwaddleRunner` object](runner.md) 
(imported from `twaddle.runner`), passing it the location of the folder containing the dictionary files 
you wish to use. Then give your [Twaddle sentences](sentences.md) to its `run_sentence` method. 

For an extremely simple example, see the `__main__.py` file. It loads dictionaries from a path provided
as an argument, or loads the default dictionary if no argument is provided, then takes twaddle sentences as
console input and prints the result:

```
from importlib.resources import files
import readline  # noqa: F401
import sys

from twaddle.exceptions import TwaddleException
from twaddle.runner import TwaddleRunner


def main():
    if len(sys.argv) < 2:
        path = files("twaddle.default_dictionary")
    else:
        path = sys.argv[1]
    twaddle = TwaddleRunner(path)

    print("hello. I'm your friendly nonsense generator. Hit Ctrl-D to exit.")

    while True:
        try:
            sentence = input(">")
            print(twaddle.run_sentence(sentence))
        except TwaddleException as te:
            print(f"Twaddle encountered an error:\n{te.message}")
            twaddle.clear()
        except EOFError:
            quit()


if __name__ == "__main__":
    main()

```
