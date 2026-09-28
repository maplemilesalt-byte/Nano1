"""Nano Power 3 CPU emulator.

Nano Power 3 v0.1 is a 4-bit CPU:
- A, B, C, D: 4-bit general-purpose registers
- PC, SP: 16-bit addresses
- Z, C flags
- 8-bit instruction words (4-bit opcode + 4-bit operand)
"""

class CPU:
    FLAG_Z = 0x01
    FLAG_C = 0x02

    def __init__(self, memory):
        self.memory = memory
        self.reset()

    def reset(self):
        self.a = self.b = self.c = self.d = 0
        self.pc = 0
        self.sp = 0xFFFF
        self.flags = 0
        self.halted = False

    def _get_reg(self, index):
        return [self.a, self.b, self.c, self.d][index & 3]

    def _set_reg(self, index, value):
        value &= 0xF
        if index == 0: self.a = value
        elif index == 1: self.b = value
        elif index == 2: self.c = value
        else: self.d = value

    def _fetch8(self):
        value = self.memory.read8(self.pc)
        self.pc = (self.pc + 1) & 0xFFFF
        return value

    def _fetch16(self):
        lo = self._fetch8()
        hi = self._fetch8()
        return lo | (hi << 8)

    def _set_zn(self, value):
        if value & 0xF:
            self.flags &= ~self.FLAG_Z
        else:
            self.flags |= self.FLAG_Z

    def step(self):
        if self.halted:
            return

        instruction = self._fetch8()
        opcode = instruction >> 4
        operand = instruction & 0xF

        if opcode == 0x0:       # NOP
            return
        elif opcode == 0x1:     # LDI r, imm4 (next byte)
            self._set_reg(operand & 3, self._fetch8() & 0xF)
        elif opcode == 0x2:     # MOV rd, rs
            self._set_reg(operand >> 2, self._get_reg(operand & 3))
        elif opcode == 0x3:     # ADD A, r
            result = self.a + self._get_reg(operand & 3)
            self.flags = (self.flags & ~self.FLAG_C) | (self.FLAG_C if result > 0xF else 0)
            self.a = result & 0xF
            self._set_zn(self.a)
        elif opcode == 0x4:     # SUB A, r
            result = self.a - self._get_reg(operand & 3)
            self.flags = (self.flags & ~self.FLAG_C) | (self.FLAG_C if result < 0 else 0)
            self.a = result & 0xF
            self._set_zn(self.a)
        elif opcode == 0x5:     # AND A, r
            self.a &= self._get_reg(operand & 3)
            self._set_zn(self.a)
        elif opcode == 0x6:     # OR A, r
            self.a |= self._get_reg(operand & 3)
            self._set_zn(self.a)
        elif opcode == 0x7:     # XOR A, r
            self.a ^= self._get_reg(operand & 3)
            self._set_zn(self.a)
        elif opcode == 0x8:     # INC r
            r = operand & 3
            self._set_reg(r, self._get_reg(r) + 1)
            self._set_zn(self._get_reg(r))
        elif opcode == 0x9:     # DEC r
            r = operand & 3
            self._set_reg(r, self._get_reg(r) - 1)
            self._set_zn(self._get_reg(r))
        elif opcode == 0xA:     # JMP addr16
            self.pc = self._fetch16()
        elif opcode == 0xB:     # JZ addr16
            addr = self._fetch16()
            if self.flags & self.FLAG_Z:
                self.pc = addr
        elif opcode == 0xC:     # LOAD A, [addr16]
            self.a = self.memory.read8(self._fetch16()) & 0xF
            self._set_zn(self.a)
        elif opcode == 0xD:     # STORE A, [addr16]
            self.memory.write8(self._fetch16(), self.a)
        elif opcode == 0xE:     # HALT
            self.halted = True
        else:
            raise RuntimeError(f"Unknown Nano Power 3 opcode: 0x{opcode:X}")

    def run(self, cycles=1000):
        for _ in range(cycles):
            if self.halted:
                break
            self.step()
