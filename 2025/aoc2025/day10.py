from boiler import AbstractDay

import re
import queue
import math

from itertools import count

from z3 import *

def work(switch, node):
    node = list(node)
    for s in switch:
        node[s] = not node[s]
    return tuple(node)


def breitensuche(init, switches, goal):
    q = queue.Queue()
    q.put((init, 0))
    seen = {init}
    while not q.empty():
        node, step = q.get()
        if node == goal:
            return step
        for switch in switches:
            next_node = work(switch, node)
            if next_node not in seen:
                q.put((next_node, step + 1))
                seen.add(next_node)

    return None



class Day10(AbstractDay):
    def preprocess(self):
        regex = re.compile(r'\[([.#]+)\] ([\(\)\d, ]+)+{([\d,]+)}')
        self.goal = []
        self.switches = []
        self.joltage = []
        for l in self.puzzle:
            m = regex.match(l)
            goal = tuple([False if c == '.' else True for c in m[1]])
            self.goal.append(goal)
            switch = [[int(i) for i in s[1:-1].split(',')] for s in m[2].split()]
            self.switches.append(switch)
            joltage = tuple([int(i) for i in m[3].split(',')])
            self.joltage.append(joltage)

        return

    def part1(self):
        res = 0
        for g, s in zip(self.goal, self.switches):
            init = tuple([False for _ in range(len(g))])
            res += breitensuche(init, s, g)
        return res

    def part2(self):
        res = 0
        for joltage, switches in zip(self.joltage, self.switches):
            s = Optimize()
            for i, jl in enumerate(joltage):
                zwerg = []
                for k, sw in enumerate(switches):
                    if i in sw:
                        v = Int(chr(k+65))
                        zwerg.append(v)
                        s.add(v >= 0)
                s.add(sum(zwerg) == jl)

            
            s.minimize(sum(Int(chr(i+65)) for i in range(len(switches))))
            s.check()
            model = s.model()

            r = 0
            for i in range(len(switches)):
                r += model[Int(chr(i +65))].as_long()

            res += r
        return res

