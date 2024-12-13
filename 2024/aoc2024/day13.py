from boiler import AbstractDay

import re
from sympy import symbols, solve, Integer

from dataclasses import dataclass
from itertools import batched


@dataclass
class Machine:
    A: (int, int)
    B: (int, int)
    p: (int, int)

_button_re = re.compile(r'Button .: X\+(\d+), Y\+(\d+)')
_prize_re = re.compile(r'Prize: X=(\d+), Y=(\d+)')

def parse_button(button):
    m = _button_re.match(button)
    return (int(m[1]), int(m[2]))

def parse_prize(prize):
    m = _prize_re.match(prize)
    return (int(m[1]), int(m[2]))

class Day13(AbstractDay):
    def preprocess(self):
        machines = []
        for batch in batched(self.puzzle, 4):
            machines.append(Machine(parse_button(batch[0]), parse_button(batch[1]), parse_prize(batch[2])))
        self.machines = machines

    def part1(self):
        res = 0
        for m in self.machines:
            a = m.A
            b = m.B
            c = m.p
            x0, x1 = symbols(['x0', 'x1'])
            sol = solve([a[0] * x0 + b[0] * x1 - c[0], a[1] * x0 + b[1] * x1 - c[1]], [x0, x1])
            if isinstance(sol[x0], Integer) and isinstance(sol[x1], Integer):
                res += 3 * int(sol[x0]) + int(sol[x1])
        return res

    def part2(self):
        res = 0
        for m in self.machines:
            a = m.A
            b = m.B
            c = (m.p[0] + 10000000000000, m.p[1] + 10000000000000 )
            x0, x1 = symbols(['x0', 'x1'])
            sol = solve([a[0] * x0 + b[0] * x1 - c[0], a[1] * x0 + b[1] * x1 - c[1]], [x0, x1])
            if isinstance(sol[x0], Integer) and isinstance(sol[x1], Integer):
                res += 3 * int(sol[x0]) + int(sol[x1])
        return res

