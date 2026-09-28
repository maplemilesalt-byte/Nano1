"""Simple Nano1 display window."""

import tkinter as tk

from .video import WIDTH, HEIGHT, get_pixel
from .input import Input


class Display:
    KEY_MAP = {"Up": Input.UP, "Down": Input.DOWN, "Left": Input.LEFT, "Right": Input.RIGHT, "Return": Input.FIRE}
    def __init__(self, vram, input_device=None, scale=4):
        self.vram = vram
        self.input = input_device or Input()
        self.scale = scale
        self.root = tk.Tk()
        self.root.title("Nano1")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH * scale,
            height=HEIGHT * scale,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.image = tk.PhotoImage(width=WIDTH, height=HEIGHT)
        self.root.bind("<KeyPress>", self._key_press)
        self.root.bind("<KeyRelease>", self._key_release)
        self.root.focus_force()
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        self.image.zoom(scale, scale)

    def _key_press(self, event):
        button = self.KEY_MAP.get(event.keysym)
        if button is not None:
            self.input.press(button)

    def _key_release(self, event):
        button = self.KEY_MAP.get(event.keysym)
        if button is not None:
            self.input.release(button)

    def refresh(self):
        rows = []
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                row.append("#000000" if get_pixel(self.vram, x, y) else "#FFFFFF")
            rows.append("{" + " ".join(row) + "}")

        self.image.put(" ".join(rows))
        self.root.after(16, self.refresh)

    def run(self):
        self.refresh()
        self.root.mainloop()
