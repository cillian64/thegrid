"""
tkinter.py

Tkinter sink to display grid status in 2D in a new window.
"""

import logging
from multiprocessing import Process, Array
from .sink import Sink, register_sink

logger = logging.getLogger(__name__)


def run_tk(arr):
    import tkinter as tk

    # Truly awful but I see no alternative.
    # If `import tkinter` runs in the outside scope, it will run in the
    # original Python process, not the new one started by multiprocessing,
    # which is enough to cause tkinter to just Not Work. Joyous.
    # http://bugs.python.org/issue5527
    # If I import it just inside the function, the class can't derive from
    # tk.Frame, so.....
    class Application(tk.Frame):
        def __init__(self, arr, master=None):
            self.arr = arr
            tk.Frame.__init__(self, master)
            self.pack()
            self.create_widgets()
            self.lights = []

        def create_widgets(self):
            self.canvas = tk.Canvas(self, width=700, height=700)
            self.canvas.create_rectangle(0, 0, 700, 700, fill="black")
            for x in range(7):
                for y in range(7):
                    xx = 50 + 100 * x
                    yy = 50 + 100 * y
                    self.canvas.create_oval(xx - 5, yy - 5, xx + 5, yy + 5,
                                            outline="white")
            self.canvas.pack()

        def draw_grid(self):
            for light in self.lights:
                self.canvas.delete(light)
            for idx, v in enumerate(self.arr):
                if v:
                    y = (idx // 7) * 100 + 50
                    x = (idx % 7) * 100 + 50
                    light = self.canvas.create_oval(
                        x - 15, y - 15, x + 15, y + 15, fill="white")
                    self.lights.append(light)
            self.after_idle(self.draw_grid)

    root = tk.Tk()
    app = Application(arr, master=root)
    root.after(100, app.draw_grid)
    app.mainloop()


@register_sink("Tkinter")
class Tkinter(Sink):
    def __init__(self):
        logger.info("Tkinter sink loading")
        self.arr = Array('b', [0]*49)
        self.process = Process(
            target=run_tk, args=(self.arr,), daemon=True)
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()

    def __del__(self):
        self.stop()

    def update(self, state):
        for idx, x in enumerate(state.reshape(-1).astype(int).tolist()):
            self.arr[idx] = x
