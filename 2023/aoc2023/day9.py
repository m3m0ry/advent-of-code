import itertools
import operator

from boiler import AbstractDay

def parse_input(puzzle):
    return [[int(i) for i in line.split()] for line in puzzle]



def extrapolate_day(values, end = True):
    direction = -1 if end else 0
    operation = operator.add if end else operator.sub
    result = 0
    for value in values:
        value_list = [value]
        while True:
            li = []
            for l, r in itertools.pairwise(value):
                li.append(r-l)
            value_list.append(li)
            value = li
            if all((x == 0 for x in li)):
                break

        fill = 0
        for line in reversed(value_list):
            if line:
                fill = operation(line[direction], fill)
        result += fill
    return result


class Day9(AbstractDay):
    def part1(self):
        values = parse_input(self.puzzle)
        return extrapolate_day(values)


    def part2(self):
        values = parse_input(self.puzzle)
        return extrapolate_day(values, end=False)

