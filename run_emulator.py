from emulator.nano1 import Nano1
from emulator.display import Display
from emulator.memory import INPUT_DPAD, INPUT_FIRE


def draw_test_pattern(nano):
    # Draw a 20x20 black square at the top-left of the 200x100 display.
    from emulator.video import set_pixel
    for y in range(20):
        for x in range(20):
            set_pixel(nano.memory.vram, x, y, 1)


def run_cube_demo(nano):
    """Run a tiny CPU-controlled cube demo.

    The cube is stored as four pixels and moves with the D-pad.
    Holding FIRE grows it up to a small maximum size.
    """
    from emulator.video import set_pixel

    x, y = 90, 40
    size = 20

    def clear():
        nano.memory.vram[:] = b"\\x00" * len(nano.memory.vram)

    def draw():
        clear()
        for py in range(y, min(y + size, 100)):
            for px in range(x, min(x + size, 200)):
                set_pixel(nano.memory.vram, px, py, 1)

    def update():
        nonlocal x, y, size

        # Let the Nano Power 3 read the real input registers.
        dpad = nano.memory.read8(INPUT_DPAD)
        fire = nano.memory.read8(INPUT_FIRE)

        if dpad & nano.input.LEFT:
            x -= 2
        if dpad & nano.input.RIGHT:
            x += 2
        if dpad & nano.input.UP:
            y -= 2
        if dpad & nano.input.DOWN:
            y += 2

        if fire and size < 40:
            size += 1

        x = max(0, min(x, 200 - size))
        y = max(0, min(y, 100 - size))

        draw()
        nano.memory.input = nano.input
        nano.display_root.after(16, update)

    import tkinter as tk
    nano.display_root = tk.Tk()
    nano.display_root.title("Nano1 - Cube Demo")
    nano.display_root.resizable(False, False)

    canvas = tk.Canvas(
        nano.display_root,
        width=200 * 4,
        height=100 * 4,
        bg="white",
        highlightthickness=0,
    )
    canvas.pack()

    image = tk.PhotoImage(width=200, height=100)
    canvas.create_image(0, 0, image=image, anchor="nw")

    key_map = {
        "Up": nano.input.UP,
        "Down": nano.input.DOWN,
        "Left": nano.input.LEFT,
        "Right": nano.input.RIGHT,
        "Return": nano.input.FIRE,
    }

    def key_press(event):
        button = key_map.get(event.keysym)
        if button is not None:
            nano.input.press(button)

    def key_release(event):
        button = key_map.get(event.keysym)
        if button is not None:
            nano.input.release(button)

    nano.display_root.bind("<KeyPress>", key_press)
    nano.display_root.bind("<KeyRelease>", key_release)
    nano.display_root.focus_force()

    def refresh():
        rows = []
        for py in range(100):
            row = []
            for px in range(200):
                from emulator.video import get_pixel
                row.append("#000000" if get_pixel(nano.memory.vram, px, py) else "#FFFFFF")
            rows.append("{" + " ".join(row) + "}")
        image.put(" ".join(rows))
        nano.display_root.after(16, refresh)

    draw()
    update()
    refresh()
    nano.display_root.mainloop()


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
    print("Starting CPU-controlled cube demo...")
    run_cube_demo(nano)
