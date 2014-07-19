import pyglet
import numpy as np
import pattern_editor


if __name__ == "__main__":
    window = pattern_editor.EditorWindow()
    dummy_state = np.zeros((7, 7), dtype=np.bool)
    dummy_state[2][3] = True
    window.griddisplay.update_grid(dummy_state)
    pyglet.app.run()
