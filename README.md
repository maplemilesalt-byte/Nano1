Nano1
=====

A fictional 4-bit handheld console.

CPU: Nano Power 3
RAM: 4 KB
VRAM: 4 KB
Display: 200x100, monochrome
Audio: 2 channels
Input: Atari-style
Cartridge: .nan
Game language: NanoLua

## Emulator

The first Nano1 cartridge game is **Fire Pixel**. Press **Enter / FIRE** to toggle the center pixel. It runs directly on the Nano Power 3 CPU. Build it with `python3 games/fire_pixel.py` and open the generated `games/fire_pixel.nan` with **File > Open Cartridge (.nan)**.\n\n## .nan cartridges\n\n`.nan` is the Nano1 cartridge format. Version 1 stores a small header followed by the raw Nano Power 3 ROM. ROM is mapped at `0x8000`, and the header contains the CPU entry point.\n\nThe emulator menu has **File > Open Cartridge (.nan)** for loading cartridges. Raw ROMs can be packaged with `tools/make_nan.py`.

Current hardware model:
- Nano Power 3: 4-bit CPU
- RAM: 4 KB
- VRAM: 4 KB
- Display: 200x100, 1-bit monochrome
- 2 audio channels (hardware model to be implemented)
- Atari-style controls (hardware model to be implemented)
- Cartridge format: .nan (NAN1 v1, implemented)
- Game language: Lua/NanoLua (after the emulator core)

The CPU ISA is currently **v0.1** and may evolve while the hardware is being defined.
