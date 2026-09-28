"""Nano1 200x100 monochrome video memory."""

WIDTH = 200
HEIGHT = 100
FRAMEBUFFER_BYTES = (WIDTH * HEIGHT + 7) // 8

def get_pixel(vram, x, y):
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return 0
    index = y * WIDTH + x
    byte = vram[index >> 3]
    return (byte >> (7 - (index & 7))) & 1

def set_pixel(vram, x, y, value):
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return
    index = y * WIDTH + x
    byte_index = index >> 3
    mask = 1 << (7 - (index & 7))
    if value:
        vram[byte_index] |= mask
    else:
        vram[byte_index] &= ~mask

def framebuffer(vram):
    """Return the 200x100 framebuffer as rows of 0/1 pixels."""
    return [
        [get_pixel(vram, x, y) for x in range(WIDTH)]
        for y in range(HEIGHT)
    ]
