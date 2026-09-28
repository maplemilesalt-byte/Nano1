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
