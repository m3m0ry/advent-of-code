from boiler import AbstractDay

import re

class Day3(AbstractDay):
    def preprocess(self):
        return

    def part1(self):
        r = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
        res = 0
        for l in self.puzzle:
            for m in r.finditer(l):
                res += int(m[1]) * int(m[2])
        return res

    def part2(self):
        r = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|don't\(\)|do\(\)")
        res = 0
        work = True
        for l in self.puzzle:
            for m in r.finditer(l):
                if m[0] == 'do()':
                    work = True
                elif m[0] == "don't()":
                    work = False
                elif work:
                    res += int(m[1]) * int(m[2])
        return res

