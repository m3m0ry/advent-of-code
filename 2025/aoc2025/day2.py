from boiler import AbstractDay

from collections import namedtuple

Range = namedtuple('Range', ['f', 'l'])



def is_invalid_id(n):
    h = len(n) // 2
    return n[0:h] == n[h:]

def invalid_ids(r):
    count = 0
    for i in range(int(r.f), int(r.l)+1):
        count += i if is_invalid_id(str(i)) else 0
    return count


def is_invalid_id_2(n):
    l = len(n)
    for i in (x for x in range(1, l//2+1) if l % x == 0):
        start = n[0:i]
        invalid = True
        for j in range(l // i):
            if start != n[j*i:(j+1)*i]:
                invalid = False

        if invalid:
            return True
    return False


def invalid_ids_2(r):
    count = 0
    for i in range(int(r.f), int(r.l)+1):
        count += i if is_invalid_id_2(str(i)) else 0
    return count


class Day2(AbstractDay):
    def preprocess(self):
        self.ranges = []
        for r in self.puzzle[0].split(','):
            f, l = r.split('-')
            self.ranges.append(Range(f, l))


    def part1(self):
        res = 0
        for r in self.ranges:
            res += invalid_ids(r)

        return res

    def part2(self):
        res = 0
        for r in self.ranges:
            res += invalid_ids_2(r)

        return res

