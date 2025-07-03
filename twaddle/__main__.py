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
