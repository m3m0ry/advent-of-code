from boiler import AbstractDay

from collections import Counter

class Day1(AbstractDay):
    def preprocess(self):
        a = []
        b = []
        for line in self.puzzle:
            x, y = line.split()
            a.append(int(x))
            b.append(int(y))
        self.a = a
        self.b = b

    def part1(self):
        a = self.a
        b = self.b
        a.sort()
        b.sort()

        return sum((abs(x - y) for x,y in zip(a,b)))

    def part2(self):
        a = self.a
        b = Counter(self.b)
        return sum((x * b[x] for x in a))

