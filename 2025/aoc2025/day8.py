from boiler import AbstractDay

from itertools import combinations

import math


def distance(i, j):
    return math.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2 + (i[2]-j[2])**2)


class Day8(AbstractDay):
    def preprocess(self):
        b = []
        for l in self.puzzle:
            b.append(tuple(int(n) for n in l.split(',')))
        self.boxes = b


        pairs = []
        for i, j in combinations(self.boxes, 2):
            pairs.append((i, j, distance(i,j)))

        pairs.sort(key=lambda x: x[2])

        self.pairs = pairs
        return

    def part1(self):
        circuits = []
        for i, j, _ in self.pairs[:1000]:
            merge = []
            impossible = []
            for c in circuits:
                if i in c or j in c:
                    merge.append(c)
                else:
                    impossible.append(c)
            circuits = impossible
            if len(merge) == 0:
                circuits.append({i, j})
            else:
                big_set = set().union(*merge)
                big_set.add(i)
                big_set.add(j)
                circuits.append(big_set)

        circuits.sort(key=lambda x: -len(x))

        res = 1
        for c in circuits[:3]:
            res *= len(c)

        return res

    def part2(self):
        last = None
        circuits = []
        for i, j, _ in self.pairs:
            last_length = len(circuits)
            merge = []
            impossible = []
            for c in circuits:
                if i in c or j in c:
                    merge.append(c)
                else:
                    impossible.append(c)
            circuits = impossible
            if len(merge) == 0:
                circuits.append({i, j})
            else:
                big_set = set().union(*merge)
                big_set.add(i)
                big_set.add(j)
                circuits.append(big_set)
            if len(circuits) == 1 and all((b in circuits[0] for b in self.boxes)):
                last = i, j
                break

        return last[0][0] * last[1][0]

