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

    NAMES = {
        UP: "UP",
        DOWN: "DOWN",
        LEFT: "LEFT",
        RIGHT: "RIGHT",
        FIRE: "FIRE",
    }

    def __init__(self, logger=None):
        self.state = 0
        self.logger = logger

    def press(self, button):
        old_state = self.state
        self.state |= button
        if self.state != old_state and self.logger is not None:
            self.logger.record("PRESS", button, self.state)

    def release(self, button):
        old_state = self.state
        self.state &= ~button
        if self.state != old_state and self.logger is not None:
            self.logger.record("RELEASE", button, self.state)

    def is_pressed(self, button):
        return bool(self.state & button)
