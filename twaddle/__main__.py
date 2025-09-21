import readline  # noqa: F401
import sys
from importlib.resources import files

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
