from boiler import AbstractDay

import re

from dataclasses import dataclass

@dataclass
class Registers:
    A: int
    B: int
    C: int

def combo(op, registers):
    match op:
        case '0':
            return 0
        case '1':
            return 1
        case '2':
            return 2
        case '3':
            return 3
        case '4':
            return registers.A
        case '5':
            return registers.B
        case '6':
            return registers.C
        case '7':
            raise NotImplementedError('7')

def ops(inst, op, registers):
    match inst:
        case '0':
            # adv
            registers.A = registers.A // 2**combo(op, registers)
        case '1':
            # bxl
            a = registers.B
            b = int(op)
            registers.B = a ^ b
        case '2':
            # bst
            registers.B = combo(op, registers) % 8
        case '3':
            # jnz
            if registers.A == 0:
                return None
            else:
                return int(op)
        case '4':
            # bxc
            a = registers.B
            b = registers.C
            registers.B = a ^ b
        case '5':
            # out
            return f'{combo(op, registers)%8}'
        case '6':
            # bdv
            registers.B = registers.A // 2**combo(op, registers)
        case '7':
            registers.C = registers.A // 2**combo(op, registers)


def run(opcode, registers):
    i = 0
    out = []
    while i < len(opcode):
        res = ops(opcode[i], opcode[i+1], registers)
        if isinstance(res, str):
            out.append(res)
            i += 2
        elif isinstance(res, int):
            i = res
        else:
            i += 2
    return out


class Day17(AbstractDay):
    def preprocess(self):
        a = int(self.puzzle[0].split()[-1])
        b = int(self.puzzle[1].split()[-1])
        c = int(self.puzzle[2].split()[-1])
        self.register = Registers(a, b, c)
        self.opcode = self.puzzle[4].split()[-1].split(',')

    def part1(self):
        registers = self.register
        opcode = self.opcode
        i = 0
        out = []
        while i < len(opcode):
            res = ops(opcode[i], opcode[i+1], registers)
            if isinstance(res, str):
                out.append(res)
                i += 2
            elif isinstance(res, int):
                i = res
            else:
                i += 2

        return ','.join(out)

    def part2(self):
        opcode = self.opcode

        nums = [0] * len(opcode)
        current = 0
        i = 0
        while i < len(opcode):
            while nums[i] < 2**6:
                test = (current << 3) + nums[i]
                out = run(opcode, Registers(test, self.register.B, self.register.C))
                if out == opcode[-len(out):]:
                    current = test
                    i += 1
                    break
                nums[i] += 1
            if i == len(opcode):
                break
            if nums[i] >= 8:
                nums[i] = 0
                i -= 1
                current = current >> 3
            else:
                nums[i] += 1

        return current

# 4 37 298


