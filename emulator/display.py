"""Simple Nano1 display window."""

import tkinter as tk

from .video import WIDTH, HEIGHT, get_pixel


class Display:
    def __init__(self, vram, scale=4):
        self.vram = vram
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

    def refresh(self):
        rows = []
        for y in range(HEIGHT):
            row = " ".join("black" if get_pixel(self.vram, x, y) else "white"
                           for x in range(WIDTH))
            rows.append(row)
        self.image.put(rows)
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        self.root.after(16, self.refresh)

    def run(self):
        self.refresh()
        self.root.mainloop()
