import re

from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum, auto

from boiler import AbstractDay

class Op(Enum):
    dash = auto()
    equal = auto()


@dataclass
class Instruction:
    label: str
    op: Op
    focal_length: int = 0


def parse_input(puzzle):
    return puzzle[0].split(',')


def parse_input2(puzzle):
    pattern = re.compile(r'(\S+)([=-])(\d*)')
    instructions = []
    for i in puzzle[0].split(','):
        match = pattern.match(i)
        g = match.groups()
        if g[1] == '-':
            instructions.append(Instruction(g[0], Op.dash))
        else:
            instructions.append(Instruction(g[0], Op.equal, int(g[2])))
    return instructions


def aoc_hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h
        

class Day15(AbstractDay):
    def part1(self):
        instructions = parse_input(self.puzzle)
        return sum((aoc_hash(i) for i in instructions))

    def part2(self):
        instructions = parse_input2(self.puzzle)
        boxes = [OrderedDict() for _ in range(256)]
        for i in instructions:
            box = boxes[aoc_hash(i.label)]
            if i.op == Op.dash and i.label in box:
                del box[i.label]
            elif i.op == Op.equal:
                box[i.label] = i.focal_length

        result = 0
        for box, b in enumerate(boxes):
            for slot, focal_length in enumerate(b.values()):
                result += (box+1) * (slot+1) * focal_length
        return result

