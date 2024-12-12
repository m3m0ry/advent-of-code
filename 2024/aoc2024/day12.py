from boiler import AbstractDay

import numpy as np
from scipy.ndimage import label

class Day12(AbstractDay):
    def preprocess(self):
        self.grid = np.array([[ord(c) for c in s] for s in self.puzzle])

    def part1(self):
        assert not np.isin(-1, self.grid), "-1 is in the array!"
        grid = np.pad(self.grid, 1, constant_values=(-1))

        up = np.roll(grid, shift=-1, axis=0)
        down = np.roll(grid, shift=1, axis=0)
        left = np.roll(grid, shift=-1, axis=1)
        right = np.roll(grid, shift=1, axis=1)

        fences = np.zeros_like(grid, dtype=int)
        fences += (grid != up)
        fences += (grid != down)
        fences += (grid != left)
        fences += (grid != right)

        unique_elements = np.unique(grid)

        res = 0
        for u in (u for u in unique_elements if u != -1):
            binary = (grid == u)
            crop = np.argwhere(binary)
            labeled, num = label(binary)
            for n in range(num):
                patch = np.argwhere(labeled == n+1)
                res += len(patch) * sum((fences[*p] for p in patch))

        return res

    def part2(self):
        assert not np.isin(-1, self.grid), "-1 is in the array!"
        grid = np.pad(self.grid, 1, constant_values=(-1))

        up = np.roll(grid, shift=-1, axis=0)
        down = np.roll(grid, shift=1, axis=0)
        left = np.roll(grid, shift=-1, axis=1)
        right = np.roll(grid, shift=1, axis=1)

        down_right = np.roll(grid, shift=(1, 1), axis=(0, 1))
        up_right = np.roll(grid, shift=(-1, 1), axis=(0, 1))
        down_left = np.roll(grid, shift=(1, -1), axis=(0, 1))
        up_left = np.roll(grid, shift=(-1, -1), axis=(0, 1))

        corners = np.zeros_like(grid, dtype=int)
        ups = (grid == up)
        downs = (grid == down)
        lefts = (grid == left)
        rights = (grid == right)

        ups_rights = (grid == up_right)
        downs_rights = (grid == down_right)
        ups_lefts = (grid == up_left)
        downs_lefts = (grid == down_left)

        # outer corner
        corners[ups & lefts & ~rights & ~downs] += 1
        corners[ups & rights & ~lefts & ~downs] += 1
        corners[downs & lefts & ~rights & ~ups] += 1
        corners[downs & rights & ~lefts & ~ups] += 1

        # inner corner
        corners[ups & lefts & ~ups_lefts] += 1
        corners[ups & rights & ~ups_rights] += 1
        corners[downs & lefts & ~downs_lefts] += 1
        corners[downs & rights & ~downs_rights] += 1


        # island
        corners[~ups & ~downs & ~lefts & ~rights] += 4

        # peaks
        corners[ups & ~downs & ~lefts & ~rights] += 2 
        corners[~ups & downs & ~lefts & ~rights] += 2 
        corners[~ups & ~downs & lefts & ~rights] += 2 
        corners[~ups & ~downs & ~lefts & rights] += 2 


        unique_elements = np.unique(grid)

        res = 0
        for u in (u for u in unique_elements if u != -1):
            binary = (grid == u)
            crop = np.argwhere(binary)
            labeled, num = label(binary)
            for n in range(num):
                patch = np.argwhere(labeled == n+1)
                res += len(patch) * sum((corners[*p] for p in patch))

        return res

