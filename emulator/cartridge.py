"""Nano1 .nan cartridge format.

Format v1:
    4 bytes  magic: b"NAN1"
    1 byte   format version: 1
    1 byte   flags/reserved
    2 bytes  entry point, little-endian
    4 bytes  ROM size, little-endian
    N bytes  ROM payload

ROM is mapped at 0x8000. The entry point is an absolute CPU address.
"""

import struct

MAGIC = b"NAN1"
VERSION = 1
HEADER_SIZE = 12
ROM_BASE = 0x8000


class CartridgeError(ValueError):
    pass


def build(rom, entry=ROM_BASE, flags=0):
    rom = bytes(rom)
    if not (ROM_BASE <= entry <= 0xFFFF):
        raise CartridgeError("entry point must be inside the ROM address space")
    if len(rom) > 0x10000 - ROM_BASE:
        raise CartridgeError("ROM is too large for the Nano1 address space")

    header = struct.pack(
        "<4sBBHI",
        MAGIC,
        VERSION,
        flags & 0xFF,
        entry & 0xFFFF,
        len(rom),
    )
    return header + rom


def load(data):
    data = bytes(data)
    if len(data) < HEADER_SIZE:
        raise CartridgeError("file is too small to be a Nano1 cartridge")

    magic, version, flags, entry, rom_size = struct.unpack(
        "<4sBBHI", data[:HEADER_SIZE]
    )

    if magic != MAGIC:
        raise CartridgeError("not a Nano1 .nan cartridge")
    if version != VERSION:
        raise CartridgeError(f"unsupported .nan version: {version}")
    if rom_size != len(data) - HEADER_SIZE:
        raise CartridgeError("ROM size in header does not match file size")
    if entry < ROM_BASE or entry >= ROM_BASE + rom_size:
        raise CartridgeError("entry point is outside the cartridge ROM")

    return {
        "version": version,
        "flags": flags,
        "entry": entry,
        "rom": data[HEADER_SIZE:],
    }


def load_file(path):
    with open(path, "rb") as file:
        return load(file.read())


def save_file(path, rom, entry=ROM_BASE, flags=0):
    with open(path, "wb") as file:
        file.write(build(rom, entry, flags))
