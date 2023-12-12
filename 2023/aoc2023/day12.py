from dataclasses import dataclass
from functools import lru_cache
from enum import StrEnum

from boiler import AbstractDay

class Spring(StrEnum):
    operational = '.'
    damaged = '#'
    unknown = '?'


@dataclass
class Line:
    springs: [Spring]
    numbers: [int]

    def __str__(self):
        return ''.join(self.springs) + ' ' + ','.join((str(i) for i in self.numbers))

    def __hash__(self):
        return hash(self.springs) + hash(self.numbers)


def parse_input(puzzle, n=1):
    springs = []
    for p in puzzle:
        spring, numbers = p.split()
        spring = tuple([Spring(s) for s in '?'.join([spring]*n)])
        numbers = tuple([int(i) for i in numbers.split(',')]*n)
        springs.append(Line(spring, numbers))
    return springs


@lru_cache
def count(line):
    if len(line.springs) == 0:
        return 1 if len(line.numbers) == 0 else 0
    if len(line.numbers) == 0:
        return 0 if Spring.damaged in line.springs else 1

    result = 0
    spring = line.springs[0]
    if spring in [Spring.operational, Spring.unknown]:
        result += count(Line(line.springs[1:], line.numbers))
    if spring in [Spring.damaged, Spring.unknown]:
        num = line.numbers[0]
        if num <= len(line.springs) and Spring.operational not in line.springs[:num] and (len(line.springs) == num or line.springs[num] != Spring.damaged):
            result += count(Line(line.springs[num+1:], line.numbers[1:]))
    return result

class Day12(AbstractDay):
    def part1(self):
        lines = parse_input(self.puzzle)

        result = 0
        for l in lines:
            result += count(l)
        return result

    def part2(self):
        lines = parse_input(self.puzzle, 5)

        result = 0
        for l in lines:
            result += count(l)
        return result

