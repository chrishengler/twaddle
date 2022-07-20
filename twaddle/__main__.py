import sys

from runner import Runner


def main():
    if len(sys.argv) < 2:
        print("argument required: path to directory containing dictionary files")
        return

    path = sys.argv[1]
    rant = Runner(path)

    print("hello")

    while True:
        sentence = input(">")
        print(rant.run_sentence(sentence))


if __name__ == "__main__":
    main()
