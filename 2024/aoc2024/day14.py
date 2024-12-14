from boiler import AbstractDay

import re

from dataclasses import dataclass

import numpy as np

@dataclass
class Robot:
    p: (int, int)
    v: (int, int)

class Day14(AbstractDay):
    def preprocess(self):
        r = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')
        robots = []
        for l in self.puzzle:
            m = r.match(l)
            robots.append(Robot((int(m[1]), int(m[2])), (int(m[3]), int(m[4]))))
        self.robots = robots

    def part1(self):
        steps = 100
        space = (103, 101)
        f = np.zeros(space, dtype=int)
        for r in self.robots:
            y = (r.p[0] + steps * r.v[0]) % space[1]
            x = (r.p[1] + steps * r.v[1]) % space[0]
            f[x,y] += 1

        up_left = f[:space[0]//2, :space[1]//2]
        up_right = f[space[0]//2+1:, space[1]//2+1:]
        down_left = f[:space[0]//2, space[1]//2+1:]
        down_right = f[space[0]//2+1:, :space[1]//2]

        return up_left.sum() * up_right.sum() * down_left.sum() * down_right.sum()

    def part2(self):
        steps = 0
        space = (103, 101)
        while True:
            steps += 1
            f = np.zeros(space, dtype=int)
            for r in self.robots:
                y = (r.p[0] + steps * r.v[0]) % space[1]
                x = (r.p[1] + steps * r.v[1]) % space[0]
                f[x,y] += 1
            if 2 not in f:
                break

        return steps

