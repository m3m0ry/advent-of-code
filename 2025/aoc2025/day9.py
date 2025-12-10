from boiler import AbstractDay

from itertools import combinations


def area(p, r):
    x0, x1 = (p[0], r[0]) if p[0] < r[0] else (r[0], p[0])
    y0, y1 = (p[1], r[1]) if p[1] < r[1] else (r[1], p[1])

    return (x1 - x0 + 1) * (y1 - y0 + 1)



class Day9(AbstractDay):
    def preprocess(self):
        points = []
        for l in self.puzzle:
            i, j = l.split(',')
            points.append((int(i),int(j)))
        self.points = points
        return

    def part1(self):
        return max(area(p, r) for p, r in combinations(self.points, 2))


    def part2(self):
        rectangles = [(p, r, area(p, r)) for p, r in combinations(self.points, 2)]
        rectangles.sort(key = lambda x: -x[2])

        for p, r, a in rectangles:
            pass

        return None

