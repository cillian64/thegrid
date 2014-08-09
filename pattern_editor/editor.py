import sys
import pattern_editor


def main():
    if len(sys.argv) != 3:
        print("Usage: {} <pattern file> <audio file>".format(sys.argv[0]))
        return

    pattern_editor.Main(sys.argv[1], sys.argv[2]).run()

if __name__ == "__main__":
    main()
