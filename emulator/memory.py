"""Nano1 memory subsystem."""

RAM_SIZE = 4 * 1024
VRAM_SIZE = 4 * 1024
VRAM_BASE = 0x1000
INPUT_BASE = 0x2000
RAM_BASE = 0x0000

class Memory:
    def __init__(self):
        self.ram = bytearray(RAM_SIZE)
        self.vram = bytearray(VRAM_SIZE)
        self.rom = bytearray()
        self.input = None

    def load_rom(self, data):
        self.rom = bytearray(data)

    def read8(self, address):
        address &= 0xFFFF
        if RAM_BASE <= address < RAM_BASE + RAM_SIZE:
            return self.ram[address]
        if VRAM_BASE <= address < VRAM_BASE + VRAM_SIZE:
            return self.vram[address - VRAM_BASE]
        if INPUT_BASE <= address < INPUT_BASE + 1 and self.input is not None:
            return self.input.state
        if address >= 0x8000 and address - 0x8000 < len(self.rom):
            return self.rom[address - 0x8000]
        return 0

    def write8(self, address, value):
        address &= 0xFFFF
        value &= 0xFF
        if RAM_BASE <= address < RAM_BASE + RAM_SIZE:
            self.ram[address] = value
        elif VRAM_BASE <= address < VRAM_BASE + VRAM_SIZE:
            self.vram[address - VRAM_BASE] = value

    def load_program(self, data, address=0):
        for i, byte in enumerate(data):
            self.write8(address + i, byte)
