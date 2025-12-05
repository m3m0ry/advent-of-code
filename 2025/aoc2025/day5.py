from boiler import AbstractDay

from itertools import takewhile, dropwhile, islice

class Day5(AbstractDay):
    def preprocess(self):
        ranges = []
        for l in takewhile(lambda x: x != "", self.puzzle):
            first, last = l.split('-')
            ranges.append((int(first), int(last)))

        ids = [int(l) for l in islice(dropwhile(lambda x: x != "", self.puzzle), 1, None)]

        self.ids = ids
        self.ranges = ranges

    def part1(self):
        res = 0
        for i in self.ids:
            for r in self.ranges:
                if i >= r[0] and i <= r[1]:
                    res += 1
                    break
        return res

    def part2(self):


        old_ranges = []
        ranges = self.ranges.copy()
        while old_ranges != ranges:
            old_ranges = list(reversed(ranges.copy())) # Reversing hack makes the order of ranges irrelevant :)
            ranges = []
            for i, r in enumerate(old_ranges):
                inside = False
                for j, p in enumerate(ranges):
                    if r[0] >= p[0] and r[1] <= p[1]: # p encloses r
                        inside = True
                    elif r[1] <= p[1] and r[1] >= p[0]: # p has higher bound then r
                        ranges[j] = (min(r[0], p[0]), p[1])
                        inside = True
                    elif r[0] >= p[0] and r[0] <= p[1]: # p has lower bound then r
                        ranges[j] = (p[0], max(r[1], p[1]))
                        inside = True

                if not inside:
                    ranges.append(r)

        res = 0
        for r in ranges:
            res += r[1] - r[0] + 1

        return res

