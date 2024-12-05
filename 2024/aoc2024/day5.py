from boiler import AbstractDay

from collections import defaultdict
from functools import cmp_to_key

def correct_ordering(rules, update):
    # why doesn't this work?
    # compare = lambda x, y: 1 if y in rules[x] else -1
    # return update == sorted(update, key=cmp_to_key(compare))
    for i in range(1,len(update)):
        u = update[i]
        if u in rules:
            for r in rules[u]:
                if r in update[:i]:
                    return False
    return True


def fix_ordering(rules, update):
    compare = lambda x, y: 1 if y in rules[x] else -1
    return sorted(update, key=cmp_to_key(compare))


class Day5(AbstractDay):
    def preprocess(self):
        rules = defaultdict(list)
        update = []
        for e, p in enumerate(self.puzzle):
            if not p:
                break
            f, t = [int(i) for i in p.split('|')]
            rules[f].append(t)
        for p in self.puzzle[e+1:]:
            update.append([int(i) for i in p.split(',')])
        self.rules = rules
        self.updates = update

    def part1(self):
        res = 0
        for u in self.updates:
            if correct_ordering(self.rules, u):
                res += u[len(u)//2]
        return res

    def part2(self):
        res = 0
        for u in self.updates:
            if not correct_ordering(self.rules, u):
                fix = fix_ordering(self.rules, u)
                res += fix[len(fix)//2]
        return res

