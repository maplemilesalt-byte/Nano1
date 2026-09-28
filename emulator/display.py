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
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        self.image.zoom(scale, scale)

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
