from boiler import AbstractDay

import numpy as np

def count(m):
    return sum((''.join(row).count('XMAS') for row in m))

def diagonalize(m):
    for i in range(1, 2*len(m)):
        yield np.diag(m, len(m)-i)


class Day4(AbstractDay):
    def preprocess(self):
        self.m = np.array([list(s) for s in self.puzzle])

    def part1(self):
        m = self.m
        res = 0
        res += count(m)
        # To be honest, i wanted fliplr, but with all these rotations it seems to work :D
        res += count(np.flip(m))
        res += count(np.rot90(m))
        res += count(np.flip(np.rot90(m)))
        res += count(diagonalize(m))
        res += count(diagonalize(np.flip(m)))
        res += count(diagonalize(np.rot90(m)))
        res += count(diagonalize(np.flip(np.rot90(m))))
        return res

    def part2(self):
        m = self.m
        m = np.pad(m, 1)
        p = ['SAM', 'MAS']
        res = 0
        for i,j in np.argwhere(m == 'A'):
            s = m[i-1:i+2,j-1:j+2] # 3x3 Stencil
            cris = np.diag(s)
            cros = np.diag(np.fliplr(s)) # Bottom-Top Second diagonal
            if ''.join(cris) in p and ''.join(cros) in p:
                res += 1
        return res

