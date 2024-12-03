from boiler import AbstractDay

import re

class Day3(AbstractDay):
    def preprocess(self):
        return

    def part1(self):
        r = re.compile(r"mul\((\d+),(\d+)\)")
        res = 0
        for l in self.puzzle:
            for m in r.finditer(l):
                res += int(m.group(1)) * int(m.group(2))
        return res

    def part2(self):
        r = re.compile(r"(mul\((\d+),(\d+)\))|(don't\(\))|(do\(\))")
        res = 0
        work = True
        for l in self.puzzle:
            for m in r.finditer(l):
                if m.group(0) == 'do()':
                    work = True
                elif m.group(0) == "don't()":
                    work = False
                elif work:
                    res += int(m.group(2)) * int(m.group(3))
        return res

