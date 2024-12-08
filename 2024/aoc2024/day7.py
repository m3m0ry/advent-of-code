from boiler import AbstractDay

from dataclasses import dataclass
from itertools import product

@dataclass
class Eq:
    res: int
    nums: [int]

def compute(nums, ops):
    res = nums[0]
    for i, op in enumerate(ops):
        if op == "+":
            res += nums[i+1]
        elif op == "*":
            res *= nums[i+1]
        elif op == "~":
            res = int(str(res) + str(nums[i+1]))
    return res

class Day7(AbstractDay):
    def preprocess(self):
        eqs = []
        for p in self.puzzle:
            res, nums = p.split(":")
            nums = nums.strip().split(' ')
            eqs.append(Eq(int(res), [int(i) for i in nums]))
        self.eqs = eqs
        

    def part1(self):
        res = 0
        for eq in self.eqs:
            for per in product('*+', repeat=len(eq.nums)-1):
                if eq.res == compute(eq.nums, per):
                    res += eq.res
                    break
        return res


    def part2(self):
        res = 0
        for eq in self.eqs:
            for per in product('*+~', repeat=len(eq.nums)-1):
                if eq.res == compute(eq.nums, per):
                    res += eq.res
                    break
        return res

