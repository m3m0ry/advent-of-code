from boiler import AbstractDay

from functools import cache
import numpy as np

def beam(g, pos):
    # go down
    pos[0] += 1
    if g.shape[0] <= pos[0] or g.shape[1] <= pos[1]:
        return
    elif g[*pos] == '^':
        g[*pos] = '*'
        right = [pos[0], pos[1]+1]
        left = [pos[0], pos[1]-1]

        beam(g, left)
        beam(g, right)
    elif g[*pos] != '*':
        beam(g, pos)


def cached(g):
    @cache
    def beam2(pos):
        # go down
        pos = pos[0]+1, pos[1]
        if g.shape[0] <= pos[0] or g.shape[1] <= pos[1]:
            return 1
        elif g[*pos] == '^':
            right = pos[0], pos[1]+1
            left = pos[0], pos[1]-1

            return beam2(left) + beam2(right)
        else:
            return beam2(pos)
    return beam2


class Day7(AbstractDay):
    def preprocess(self):
        self.grid = np.array([[c for c in l] for l in self.puzzle])
        self.start = np.argwhere(self.grid == 'S')[0]
        return

    def part1(self):
        res = 0
        g = self.grid.copy()
        s = self.start.copy()
        beam(g, s)

        for l in g:
            for c in l:
                if c == '*':
                    res += 1
        return res

    def part2(self):
        beam2 = cached(self.grid)
        s = tuple(i for i in self.start.tolist())
        return beam2(tuple(s))

