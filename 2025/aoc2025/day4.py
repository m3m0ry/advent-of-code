from boiler import AbstractDay

import numpy as np

class Day4(AbstractDay):
    def preprocess(self):
        return

    def part1(self):
        grid = np.array([list(l) for l in self.puzzle])
        grid = np.pad(grid, 1)
        left = (np.roll(grid, -1) == '@').astype(int)
        right = (np.roll(grid, 1) == '@').astype(int)
        up = (np.roll(grid, -1, axis=0) == '@').astype(int)
        down = (np.roll(grid, 1, axis=0) == '@').astype(int)
        left_up = (np.roll(grid, (-1, -1), axis=(0, 1)) == '@').astype(int)
        left_down = (np.roll(grid, (1, -1), axis=(0, 1)) == '@').astype(int)
        right_up = (np.roll(grid, (-1, 1), axis=(0, 1)) == '@').astype(int)
        right_down = (np.roll(grid, (1, 1), axis=(0, 1)) == '@').astype(int)

        res = left + right + up + down + left_up + left_down + right_up + right_down
        accessed = np.logical_and(res < 4, grid == '@')[1:-1, 1:-1]
        return np.count_nonzero(accessed)

    def part2(self):
        result = 0
        grid = np.array([list(l) for l in self.puzzle])
        grid = np.pad(grid, 1)

        i = 0
        while True:
            left = (np.roll(grid, -1) == '@').astype(int)
            right = (np.roll(grid, 1) == '@').astype(int)
            up = (np.roll(grid, -1, axis=0) == '@').astype(int)
            down = (np.roll(grid, 1, axis=0) == '@').astype(int)
            left_up = (np.roll(grid, (-1, -1), axis=(0, 1)) == '@').astype(int)
            left_down = (np.roll(grid, (1, -1), axis=(0, 1)) == '@').astype(int)
            right_up = (np.roll(grid, (-1, 1), axis=(0, 1)) == '@').astype(int)
            right_down = (np.roll(grid, (1, 1), axis=(0, 1)) == '@').astype(int)

            res = left + right + up + down + left_up + left_down + right_up + right_down
            accessed = np.logical_and(res < 4, grid == '@')
            grid[accessed] = 'x'

            removed = np.count_nonzero(accessed[1:-1, 1:-1])
            i += 1
            if removed == 0:
                return result
            else:
                result += removed

