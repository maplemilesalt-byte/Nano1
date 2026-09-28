"""Top-level Nano1 machine."""

from .cpu import CPU
from .memory import Memory
from .input import Input
from .input_logger import InputLogger

class Nano1:
    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.input_logger = InputLogger()
        self.input = Input(self.input_logger)
        self.memory.input = self.input

    def reset(self):
        self.cpu.reset()
        self.input.state = 0
        self.input_logger.clear()

    def load_program(self, program, address=0):
        self.memory.load_program(program, address)
        self.cpu.pc = address

    def run(self, cycles=1000):
        self.cpu.run(cycles)
