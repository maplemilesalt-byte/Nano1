#!/usr/bin/env python3
"""Build a Nano1 .nan cartridge from a raw ROM binary."""

import argparse

from emulator.cartridge import ROM_BASE, save_file


def main():
    parser = argparse.ArgumentParser(description="Build a Nano1 .nan cartridge")
    parser.add_argument("rom", help="raw Nano Power 3 ROM binary")
    parser.add_argument("output", help="output .nan file")
    parser.add_argument(
        "--entry",
        type=lambda value: int(value, 0),
        default=ROM_BASE,
        help="CPU entry address (default: 0x8000)",
    )
    args = parser.parse_args()

    with open(args.rom, "rb") as file:
        rom = file.read()

    save_file(args.output, rom, args.entry)
    print(f"Built {args.output}: {len(rom)} ROM bytes, entry 0x{args.entry:04X}")


if __name__ == "__main__":
    main()
