from boiler import AbstractDay

import re
import queue


def compute(op, registers):
    match op[0]:
        case 'AND':
            registers[op[1]] = registers[op[2]] and registers[op[3]]
        case 'OR':
            registers[op[1]] = registers[op[2]] or registers[op[3]]
        case 'XOR':
            registers[op[1]] = registers[op[2]] ^ registers[op[3]]
        case _:
            raise NotImplementedError('No such op!')

class Day24(AbstractDay):
    def preprocess(self):
        x = 0
        for i, l in enumerate(self.puzzle):
            if not l:
                x = i
                break
        
        registers = {}
        for l in self.puzzle[:x]:
            reg, num = l.split(': ')
            registers[reg] = bool(int(num))
        
        pattern = re.compile(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)')
        ops = []
        for l in self.puzzle[x+1:]:
            m = pattern.match(l)
            ops.append((m[2], m[4], m[1], m[3]))

        self.registers = registers
        self.ops = ops

    def part1(self):
        regs = self.registers
        ops = self.ops
        ops_queue = queue.SimpleQueue()
        for op in ops:
            ops_queue.put(op)

        while not ops_queue.empty():
            op = ops_queue.get()
            if op[2] in regs and op[3] in regs:
                compute(op, regs)
            else:
                ops_queue.put(op)

        zs = [reg for reg in regs if 'z' == reg[0]]
        zs.sort()
        num = ''.join(str(int(regs[i])) for i in reversed(zs))

        return int(num, 2)

    def part2(self):
        return None

