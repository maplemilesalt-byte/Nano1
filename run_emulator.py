from emulator.nano1 import Nano1
from emulator.display import Display
from emulator.memory import INPUT_DPAD, INPUT_FIRE


def draw_test_pattern(nano):
    # Draw a 20x20 black square at the top-left of the 200x100 display.
    from emulator.video import set_pixel
    for y in range(20):
        for x in range(20):
            set_pixel(nano.memory.vram, x, y, 1)


def cpu_test():
    nano = Nano1()
    # LDI A, 3 ; LDI B, 5 ; ADD A, B ; HALT
    program = bytes([0x10, 0x03, 0x11, 0x05, 0x31, 0xE0])
    nano.load_program(program)
    nano.run()

    if nano.cpu.a != 8:
        raise AssertionError(f"Expected A=8, got A={nano.cpu.a}")

    return nano.cpu.a


def input_test():
    nano = Nano1()

    # D-pad: RIGHT = 0x08 at 0x2000.
    nano.input.press(nano.input.RIGHT)
    program = bytes([0xC0, 0x00, 0x20, 0xE0])  # LOAD A, [0x2000] ; HALT
    nano.load_program(program)
    nano.run()
    if nano.cpu.a != 0x08:
        raise AssertionError(f"Expected CPU to read RIGHT=0x08, got 0x{nano.cpu.a:02X}")

    nano.reset()

    # FIRE is a separate 0/1 register at 0x2001 because the CPU is 4-bit.
    nano.input.press(nano.input.FIRE)
    program = bytes([0xC0, 0x01, 0x20, 0xE0])  # LOAD A, [0x2001] ; HALT
    nano.load_program(program)
    nano.run()
    if nano.cpu.a != 1:
        raise AssertionError(f"Expected CPU to read FIRE=1, got {nano.cpu.a}")

    return nano.cpu.a


def vram_test():
    nano = Nano1()
    # Write 1 to the first VRAM byte through the CPU.
    # LDI A, 1 ; STORE A, [0x1000] ; HALT
    program = bytes([0x10, 0x01, 0xD0, 0x00, 0x10, 0xE0])
    nano.load_program(program)
    nano.run()
    if nano.memory.vram[0] != 1:
        raise AssertionError(f"Expected VRAM[0]=1, got {nano.memory.vram[0]}")
    from emulator.video import get_pixel
    if get_pixel(nano.memory.vram, 0, 0) != 0:
        raise AssertionError("Expected pixel (0, 0) to remain OFF for VRAM byte 0x01")
    return nano.memory.vram[0]


def memory_test():
    nano = Nano1()
    # LDI A, 10 ; STORE A, [0x0200] ; LDI A, 0 ; LOAD A, [0x0200] ; HALT
    program = bytes([0x10, 0x0A, 0xD0, 0x00, 0x02, 0x10, 0x00, 0xC0, 0x00, 0x02, 0xE0])
    nano.load_program(program)
    nano.run()
    if nano.cpu.a != 0x0A:
        raise AssertionError(f"Expected RAM value 10, got {nano.cpu.a}")
    return nano.cpu.a


if __name__ == "__main__":
    nano = Nano1()

    print("Nano1 emulator booted.")
    print("CPU: Nano Power 3 (4-bit)")
    print(f"RAM: {len(nano.memory.ram)} bytes")
    print(f"VRAM: {len(nano.memory.vram)} bytes")
    print()
    print("Running CPU test...")

    result = cpu_test()

    print("A = 3")
    print("B = 5")
    print(f"A + B = {result}")
    print()
    print("CPU test passed.")
    print()
    print("Running RAM test...")
    value = memory_test()
    print("Stored A = 10")
    print(f"Loaded A = {value}")
    print()
    print("RAM test passed.")
    print()
    print("Running VRAM test...")
    vram = vram_test()
    print(f"VRAM[0] = {vram}")
    print("VRAM write test passed.")
    print()
    print("Running input test...")
    input_value = input_test()
    print(f"CPU input read = {input_value}")
    print("Input test passed.")
    print()
    print(f"Input D-pad register = 0x{INPUT_DPAD:04X}")
    print(f"Input FIRE register = 0x{INPUT_FIRE:04X}")
    print()
    print("Drawing 20x20 display test pattern...")
    draw_test_pattern(nano)
    print("Starting Nano1 display...")
    Display(nano.memory.vram, nano.input).run()
