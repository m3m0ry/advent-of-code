from boiler import AbstractDay

from itertools import combinations

from collections import defaultdict

class Day23(AbstractDay):
    def preprocess(self):
        self.graph = defaultdict(lambda: set())
        for p in self.puzzle:
            p1, p2 = p.split('-')
            self.graph[p1].add(p2)
            self.graph[p2].add(p1)
        
        for k,v in self.graph.items():
            self.graph[k] = frozenset(v)

    def part1(self):
        graph = self.graph

        sets = set()
        for node in graph:
            for x, y in combinations(graph[node], 2):
                if y in graph[x]:
                    sets.add(frozenset([node, x, y]))

        res = 0
        for s in sets:
            if any('t' == n[0] for n in s):
                res += 1

        return res

    def part2(self):
        graph = self.graph

        biggest_clique = set()
        for node in graph:
            clique = set([node])
            candidates = set(graph[node])
            while len(candidates) > 0:
                test = candidates.pop()
                if all(test in graph[x] for x in clique):
                    clique.add(test)
                    candidates |= set(x for x in graph[test] if x not in clique)
            
            if len(biggest_clique) < len(clique):
                biggest_clique = clique

        return ','.join(sorted(biggest_clique))

