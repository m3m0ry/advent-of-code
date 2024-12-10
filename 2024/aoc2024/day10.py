from boiler import AbstractDay

import numpy as np

def gimme_nines(zero, grid):
    if grid[*zero] == 9:
        return {(int(zero[0]), int(zero[1]))}

    x = np.array([1, 0])
    y = np.array([0, 1])
    pos = set()
    for p in [zero - x, zero + x, zero - y, zero + y]:
        if (grid[*p] - grid[*zero]) == 1:
            pos |= gimme_nines(p, grid)
    return pos
            

def gimme_nines2(zero, grid):
    if grid[*zero] == 9:
        return 1

    x = np.array([1, 0])
    y = np.array([0, 1])
    pos = 0
    for p in [zero - x, zero + x, zero - y, zero + y]:
        if (grid[*p] - grid[*zero]) == 1:
            pos += gimme_nines2(p, grid)
    return pos


class Day10(AbstractDay):
    def preprocess(self):
        self.grid = np.array([[int(c) if c != '.' else -1 for c in s] for s in self.puzzle])

    def part1(self):
        grid = np.pad(self.grid, 1, constant_values=(-1))
        zeros = np.argwhere(grid == 0)
        trailheads = []
        for zero in zeros:
            trailheads.append(gimme_nines(zero, grid))

        res = 0
        for trailhead in trailheads:
            res += len(trailhead)

        return res

    def part2(self):
        grid = np.pad(self.grid, 1, constant_values=(-1))
        zeros = np.argwhere(grid == 0)
        trailheads = []
        for zero in zeros:
            trailheads.append(gimme_nines2(zero, grid))

        res = 0
        for trailhead in trailheads:
            res += trailhead

        return res

