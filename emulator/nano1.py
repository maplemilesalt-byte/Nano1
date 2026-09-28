"""Top-level Nano1 machine."""

from .cpu import CPU
from .memory import Memory
from .input import Input

class Nano1:
    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.input = Input()

    def reset(self):
        self.cpu.reset()
        self.input.state = 0

    def load_program(self, program, address=0):
        self.memory.load_program(program, address)
        self.cpu.pc = address

    def run(self, cycles=1000):
        self.cpu.run(cycles)
