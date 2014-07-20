import sys
import numpy as np
import pattern_editor


def main():
    if len(sys.argv) != 3:
        print("Usage: {} <pattern file> <audio file>".format(sys.argv[0]))
        return

    main = pattern_editor.Main(sys.argv[1], sys.argv[2])

    dummy_state = np.zeros((7, 7), dtype=np.bool)
    dummy_state[2][3] = True
    main.window.griddisplay.state = dummy_state

    main.run()

if __name__ == "__main__":
    main()
