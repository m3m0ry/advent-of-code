import bisect
import itertools

import numpy as np

from boiler import AbstractDay

def solve(puzzle, n = 1):
    puzzle = np.array([[0 if c == '.' else 1 for c in line]  for line in puzzle]) 
    expand_cols = list(filter(lambda x: x, (i if t else t for i,t in enumerate(~ np.any(puzzle, axis=0)))))
    expand_rows = list(filter(lambda x: x, (i if t else t for i,t in enumerate(~ np.any(puzzle, axis=1)))))
    coords = list(zip(*np.where(puzzle)))

    new_coords = []
    for x, y in coords:
        i = bisect.bisect(expand_rows, x)
        j = bisect.bisect(expand_cols, y)
        new_coords.append((x+i*n,y+j*n))

    result = 0
    for a, b in itertools.combinations(new_coords, 2):
        i,j = a
        x,y = b
        result += abs(i-x) + abs(j-y)
    return result

class Day11(AbstractDay):
    def part1(self):
        return solve(self.puzzle)

    def part2(self):
        return solve(self.puzzle, 1000000 -1)

