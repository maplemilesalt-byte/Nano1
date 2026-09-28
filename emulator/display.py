"""Simple Nano1 display window."""

import tkinter as tk

from .video import WIDTH, HEIGHT, get_pixel
from .input import Input


class Display:
    KEY_MAP = {
        "Up": Input.UP,
        "Down": Input.DOWN,
        "Left": Input.LEFT,
        "Right": Input.RIGHT,
        "Return": Input.FIRE,
    }

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

        self.input_frame = tk.Frame(self.root, padx=8, pady=6)
        self.input_frame.pack(fill="x")

        self.input_labels = {}
        for name, button in (
            ("UP", Input.UP),
            ("DOWN", Input.DOWN),
            ("LEFT", Input.LEFT),
            ("RIGHT", Input.RIGHT),
            ("FIRE", Input.FIRE),
        ):
            label = tk.Label(
                self.input_frame,
                text=f"{name}: OFF",
                width=10,
                relief="sunken",
                bd=1,
            )
            label.pack(side="left", padx=2)
            self.input_labels[button] = label

        self.input_state_label = tk.Label(
            self.root,
            text="INPUT: 0x00",
            anchor="w",
            padx=8,
            pady=3,
        )
        self.input_state_label.pack(fill="x")

    def _key_press(self, event):
        button = self.KEY_MAP.get(event.keysym)
        if button is not None:
            self.input.press(button)

    def _key_release(self, event):
        button = self.KEY_MAP.get(event.keysym)
        if button is not None:
            self.input.release(button)

    def _update_input_display(self):
        for button, label in self.input_labels.items():
            name = Input.NAMES[button]
            state = "ON" if self.input.is_pressed(button) else "OFF"
            label.config(text=f"{name}: {state}")

        self.input_state_label.config(text=f"INPUT: 0x{self.input.state:02X}")

    def refresh(self):
        rows = []
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                row.append("#000000" if get_pixel(self.vram, x, y) else "#FFFFFF")
            rows.append("{" + " ".join(row) + "}")

        self.image.put(" ".join(rows))
        self._update_input_display()
        self.root.after(16, self.refresh)

    def run(self):
        self.refresh()
        self.root.mainloop()
