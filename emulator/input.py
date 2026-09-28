"""Nano1 input device.

Keyboard mapping:
- Arrow keys: directional input
- Enter: FIRE / shoot
"""

class Input:
    UP = 0x01
    DOWN = 0x02
    LEFT = 0x04
    RIGHT = 0x08
    FIRE = 0x10

    def __init__(self):
        self.state = 0

    def press(self, button):
        self.state |= button

    def release(self, button):
        self.state &= ~button

    def is_pressed(self, button):
        return bool(self.state & button)
