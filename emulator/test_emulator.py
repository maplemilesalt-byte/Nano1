import unittest

from .nano1 import Nano1

class Nano1Tests(unittest.TestCase):
    def test_4bit_add(self):
        nano = Nano1()
        # LDI A, 3 ; LDI B, 5 ; ADD A, B ; HALT
        program = bytes([0x13, 0x15, 0x31, 0xE0])
        nano.load_program(program)
        nano.run()
        self.assertEqual(nano.cpu.a, 8)

    def test_vram_pixel(self):
        nano = Nano1()
        from .video import get_pixel, set_pixel
        set_pixel(nano.memory.vram, 10, 10, 1)
        self.assertEqual(get_pixel(nano.memory.vram, 10, 10), 1)

if __name__ == "__main__":
    unittest.main()
