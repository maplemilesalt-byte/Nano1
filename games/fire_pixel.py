"""Nano1 first cartridge game: Fire Pixel.

Press FIRE (Enter) to toggle the target pixel.
The game runs entirely on the Nano Power 3 CPU.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emulator.cartridge import save_file

# Nano Power 3 ROM, loaded at 0x8000.
#
# 0x8000: B = 8
# 0x8002: A = 8
# 0x8004: VRAM[0x14EE] = A   (center pixel)
# 0x8007: wait for FIRE
# 0x800D: toggle center pixel
# 0x8014: wait for FIRE release
ROM = bytes([
    0x11, 0x08,             # LDI B, 8
    0x10, 0x08,             # LDI A, 8
    0xD0, 0xEE, 0x14,       # STORE A, [0x14EE]
    0xC0, 0x01, 0x20,       # LOAD A, [INPUT_FIRE]
    0xB0, 0x07, 0x80,       # JZ 0x8007
    0xC0, 0xEE, 0x14,       # LOAD A, [0x14EE]
    0x71,                   # XOR A, B
    0xD0, 0xEE, 0x14,       # STORE A, [0x14EE]
    0xC0, 0x01, 0x20,       # LOAD A, [INPUT_FIRE]
    0xB0, 0x07, 0x80,       # JZ 0x8007
    0xA0, 0x14, 0x80,       # JMP 0x8014
])


def build(output="fire_pixel.nan"):
    save_file(output, ROM)
    print(f"Built {output} ({len(ROM)} bytes of ROM)")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else str(
        Path(__file__).with_suffix(".nan")
    )
    build(output)
