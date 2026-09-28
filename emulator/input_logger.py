"""Nano1 input event logger.

Records button press/release events and the input state after each event.
"""

class InputLogger:
    def __init__(self):
        self.events = []

    def record(self, action, button, state):
        self.events.append({
            "action": action,
            "button": button,
            "state": state,
        })

    def clear(self):
        self.events.clear()

    def last(self):
        return self.events[-1] if self.events else None

    def dump(self):
        return list(self.events)
