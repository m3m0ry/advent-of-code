from boiler import AbstractDay

from itertools import combinations

import numpy as np

def is_valid_index(array, row, col):
    """Check if (row, col) is inside the array."""
    rows, cols = array.shape
    return 0 <= row < rows and 0 <= col < cols

class Day8(AbstractDay):
    def preprocess(self):
        self.grid = np.array([list(s) for s in self.puzzle])

    def part1(self):
        grid = self.grid
        signal = np.full(grid.shape, '.')
        u = np.unique(grid)
        unique = u[u != '.']
        for antenna in unique:
            indices = np.argwhere(grid == antenna)
            for a, b in combinations(indices, 2):
                diff = a-b
                poss = [a+diff, a-diff, b+diff, b-diff]
                for t in poss:
                    if (t != a).all() and (t!= b).all() and is_valid_index(grid, *t):
                        signal[*t] = '#'

        return np.count_nonzero(signal == '#')

    def part2(self):
        grid = self.grid
        signal = np.full(grid.shape, '.')
        u = np.unique(grid)
        unique = u[u != '.']
        for antenna in unique:
            indices = np.argwhere(grid == antenna)
            for a, b in combinations(indices, 2):
                diff = a-b
                poss = [(a,diff), (a,-diff), (b,+diff), (b,-diff)]
                for c, d in poss:
                    times = 0
                    t = c + d * times
                    while is_valid_index(grid, *t):
                        signal[*t] = '#'
                        times += 1
                        t = c + d * times

        return np.count_nonzero(signal == '#')

