import itertools
import numpy as np

from boiler import AbstractDay

def parse_input(puzzle):
    patterns = []
    for k, g in itertools.groupby(puzzle, lambda x: not x):
        if not k:
            patterns.append(np.array([list(l) for l in g]))

    return patterns

def mirror_line(pattern):
    rows, cols = pattern.shape
    for i in range(1, cols):
        max_cols = min(i, cols -i)
        left = pattern[:,i-max_cols:i]
        right = pattern[:, i+max_cols-1:i-1:-1]

        if np.array_equal(left, right):
            return 0, i

    for i in range(1, rows):
        max_rows = min(i, rows -i)
        left = pattern[i-max_rows:i,:]
        right = pattern[i+max_rows-1:i-1:-1,:]

        if np.array_equal(left, right):
            return i, 0
    return 0, 0

def smudge_line(pattern):
    rows, cols = pattern.shape
    for i in range(1, cols):
        max_cols = min(i, cols -i)
        left = p[:,i-max_cols:i]
        right = p[:, i+max_cols-1:i-1:-1]

        if not np.array_equal(left, right) and np.sum(left != right) == 1:
            return 0, i

    for i in range(1, rows):
        max_rows = min(i, rows -i)
        left = p[i-max_rows:i,:]
        right = p[i+max_rows-1:i-1:-1,:]

        if not np.array_equal(left, right) and np.sum(left != right) == 1:
            return i, 0
    return 0, 0

class Day13(AbstractDay):
    def part1(self):
        patterns = parse_input(self.puzzle)

        result = 0
        for p in patterns:
            rows, columns = mirror_line(p)
            result += rows*100 + columns
        return result


    def part2(self):
        patterns = parse_input(self.puzzle)

        result = 0
        for p in patterns:
            rows, columns = smudge_line(p)
            result += rows*100 + columns
        return result


