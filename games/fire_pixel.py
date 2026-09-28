"""Nano1 first cartridge game: Fire Pixel.

A tiny monochrome scene built from simple 4-bit-friendly sprites.

- A target frame surrounds the flame.
- A small spark floats above it.
- Hold FIRE (Enter) to light the flame.
- Release FIRE to return to the dim flame.

The game runs entirely on the Nano Power 3 CPU.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emulator.cartridge import save_file

VRAM_BASE = 0x1000
INPUT_FIRE = 0x2001
VRAM_ROW_BYTES = 25


def vram_addr(x_byte, y):
    return VRAM_BASE + y * VRAM_ROW_BYTES + x_byte


def ldi(register, value):
    return bytes([0x10 | register, value & 0x0F])


def store(address):
    return bytes([0xD0, address & 0xFF, (address >> 8) & 0xFF])


def load(address):
    return bytes([0xC0, address & 0xFF, (address >> 8) & 0xFF])


def jz(address):
    return bytes([0xB0, address & 0xFF, (address >> 8) & 0xFF])


def jmp(address):
    return bytes([0xA0, address & 0xFF, (address >> 8) & 0xFF])


def draw_sprite(rom, x_byte, y, pixels):
    """Append a sprite to the ROM bytearray."""
    for row, pixels4 in enumerate(pixels):
        rom += ldi(0, pixels4)
        rom += store(vram_addr(x_byte, y + row))


TARGET_LEFT = (0xF, 0x1, 0x1, 0x1, 0x1, 0x1, 0xF)
TARGET_RIGHT = (0xF, 0x8, 0x8, 0x8, 0x8, 0x8, 0xF)
SPARK = (0x4, 0x0, 0xE, 0x0, 0x4)
FLAME_DIM = (0x0, 0x4, 0x6, 0xE, 0x6, 0x4, 0x0)
FLAME_BRIGHT = (0x0, 0xE, 0xF, 0xF, 0xF, 0xE, 0x4)


def build_rom():
    rom = bytearray()

    draw_sprite(rom, 10, 40, TARGET_LEFT)
    draw_sprite(rom, 13, 40, TARGET_RIGHT)
    draw_sprite(rom, 15, 35, SPARK)
    draw_sprite(rom, 12, 43, FLAME_DIM)

    wait = 0x8000 + len(rom)
    rom += load(INPUT_FIRE)
    press_jump = len(rom)
    rom += jz(0)

    draw_sprite(rom, 12, 43, FLAME_BRIGHT)

    release = 0x8000 + len(rom)
    rom += load(INPUT_FIRE)
    release_jump = len(rom)
    rom += jz(0)
    rom += jmp(release)

    dim_after = 0x8000 + len(rom)
    draw_sprite(rom, 12, 43, FLAME_DIM)
    rom += jmp(wait)

    rom[press_jump + 1] = wait & 0xFF
    rom[press_jump + 2] = (wait >> 8) & 0xFF
    rom[release_jump + 1] = dim_after & 0xFF
    rom[release_jump + 2] = (dim_after >> 8) & 0xFF

    return bytes(rom)


ROM = build_rom()


def build(output="fire_pixel.nan"):
    save_file(output, ROM)
    print(f"Built {output} ({len(ROM)} bytes of ROM)")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else str(
        Path(__file__).with_suffix(".nan")
    )
    build(output)
