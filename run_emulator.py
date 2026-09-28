from emulator.nano1 import Nano1

if __name__ == "__main__":
    nano = Nano1()
    print("Nano1 emulator booted.")
    print(f"CPU: Nano Power 3 (4-bit)")
    print(f"RAM: {len(nano.memory.ram)} bytes")
    print(f"VRAM: {len(nano.memory.vram)} bytes")
