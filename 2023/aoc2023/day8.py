import itertools
import re
import math

from dataclasses import dataclass

@dataclass
class LR:
    self: str
    left: str
    right: str

@dataclass
class LeftRight:
    left: int
    right: int

from boiler import AbstractDay

def parse_input(puzzle):
    instructions = [True if c == 'L' else False for c in puzzle[0].strip()]

    pattern = re.compile(r'(\S\S\S) = \((\S\S\S), (\S\S\S)\)')

    lrs = []
    for p in puzzle[2:]:
        matches = pattern.fullmatch(p).groups()
        lrs.append(LR(matches[0], matches[1], matches[2]))

    left_rights = []
    aaa = -1
    zzz = -1
    ass = []
    zss = []
    for i in range(len(lrs)):
        left = -1
        right = -1
        if lrs[i].self == 'AAA':
            aaa = i
        if lrs[i].self == 'ZZZ':
            zzz = i
        if lrs[i].self[2] == 'A':
            ass.append(i)
        if lrs[i].self[2] == 'Z':
            zss.append(i)
        for j in range(len(lrs)):
            if lrs[j].self == lrs[i].left:
                left = j
            if lrs[j].self == lrs[i].right:
                right = j
            if left != -1 and right != -1:
                break

        left_rights.append(LeftRight(left, right))

    return instructions, left_rights, aaa, zzz, ass, zss


class Day8(AbstractDay):
    def part1(self):
        instructions, lrs, current, zzz, _, _ = parse_input(self.puzzle)
        for step, instruction in enumerate(itertools.cycle(instructions)):
            if current == zzz:
                return step
            if instruction:
                current = lrs[current].left
            else:
                current = lrs[current].right
        return None

    def part2(self):
        instructions, lrs, _, _, currents, zss = parse_input(self.puzzle)
        steps = []
        for current in currents:
            for step, instruction in enumerate(itertools.cycle(instructions)):
                if current in zss:
                    steps.append(step)
                    break
                if instruction:
                    current = lrs[current].left
                else:
                    current = lrs[current].right
        return math.lcm(*steps)


