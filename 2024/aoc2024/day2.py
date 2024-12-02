from boiler import AbstractDay
from collections import Counter



def match(a: list[int]):
    diff = [i-j for i,j in zip(a, a[1:])]
    if all((d > 0 for d in diff)) or all((d < 0 for d in diff)):
        if all((1 <= abs(d) <= 3 for d in diff)):
            return True
    return False


class Day2(AbstractDay):
    def preprocess(self):
        self.a = [[int(n) for n in line.split()] for line in self.puzzle]

    def part1(self):
        return sum((1 for r in self.a if match(r)))

    def part2(self):
        result = 0
        for a in self.a:
            if match(a):
                result += 1
            else:
                for i in range(len(a)):
                    b = a[:i] + a[i+1:]
                    if match(b):
                        result += 1
                        break
            #else:
            #    diff = [i-j for i,j in zip(a, a[1:])]

            #    greater_zero = [d > 0 for d in diff]
            #    jump = [1 <= d <= 3 for d in diff]
            #    gr = [j and g for j,g in zip(jump, greater_zero)]

            #    less_zero = [d < 0 for d in diff]
            #    jump_neg = [1 <= -d <= 3 for d in diff]
            #    ls = [j and l for j,l in zip(jump_neg, less_zero)]

            #    if sum((1 for l in gr if not l)) <= 3:
            #        # Try to ignore "middle" false
            #        pass
            #    elif sum((1 for l in ls if not l)) <= 3:
            #        # Try to ignore "middle" false
            #        pass

        return result

