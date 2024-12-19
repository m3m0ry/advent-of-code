from boiler import AbstractDay

import functools

def find_possible(design, towels, part=1):
    if part == 1:
        @functools.cache
        def possible(design: str):
            if len(design) == 0:
                return True

            for towel in towels:
                if design.startswith(towel):
                    if possible(design[len(towel):]):
                        return True

            return False
        return possible(design)

    else:
        @functools.cache
        def amount_possible(design: str):
            if len(design) == 0:
                return 1

            res = 0
            for towel in towels:
                if design.startswith(towel):
                    res += amount_possible(design[len(towel):])

            return res
        return amount_possible(design)


class Day19(AbstractDay):
    def preprocess(self):
        self.towels = self.puzzle[0].split(', ')
        self.designs = self.puzzle[2:]

    def part1(self):
        towels = self.towels
        designs = self.designs

        res = 0
        for design in designs:
            if find_possible(design, towels):
                res += 1
        return res

    def part2(self):
        towels = self.towels
        designs = self.designs

        res = 0
        for design in designs:
            res += find_possible(design, towels, part=2)
        return res

