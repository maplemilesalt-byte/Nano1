from emulator.nano1 import Nano1

def cpu_test():
    nano = Nano1()
    # LDI A, 3 ; LDI B, 5 ; ADD A, B ; HALT
    program = bytes([0x10, 0x03, 0x11, 0x05, 0x31, 0xE0])
    nano.load_program(program)
    nano.run()

    if nano.cpu.a != 8:
        raise AssertionError(f"Expected A=8, got A={nano.cpu.a}")

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
