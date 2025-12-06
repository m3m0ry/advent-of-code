from boiler import AbstractDay

from itertools import batched
import operator
import numpy as np

class Day6(AbstractDay):
    def __init__(self, puzzle: [str]):
        self.puzzle = [i for i in puzzle] # starting space is important in part 2

    def preprocess(self):
        self.numbers = np.array([[int(d) for d in l.split()]for l in self.puzzle[:-1]])
        self.ops = self.puzzle[-1].split()


        self.grid = np.array([[c for c in l[:-1]] for l in self.puzzle])
        return

    def part1(self):
        res = 0
        for i, op in enumerate(self.ops):
            column = self.numbers[:, i]
            if op == '+':
                res += np.sum(column)
            elif op == '*':
                res += np.prod(column)
            else:
                raise ValueError(op)
        return res

    def part2(self):
        res = 0
        current_op = None
        r = 0
        g = self.grid
        rows, columns = g.shape
        for c in range(columns):
            if (op := g[rows-1,c]) != ' ': # new column
                current_op = operator.add if op == '+' else operator.mul
                r = 0 if op == '+' else 1
            s = ''.join(g[:-1, c])
            if s.isspace():
                res += r
            else:
                r = current_op(r, int(s))
        res += r


        return res

