from boiler import AbstractDay

import math

from collections import defaultdict, Counter
from heapq import heappop, heappush

import numpy as np

def dijkstra(start, goal, grid):
    h = []
    heappush(h, (0, start))

    prev = dict()

    dist = defaultdict(lambda: math.inf)
    dist[start] = 0

    while h:
        current = heappop(h)[1]

        for neighbor in neighbors(current, grid):
            alt = dist[current] + 1
            if alt < dist[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                prev[neighbor] = current
                dist[neighbor] = alt
                heappush(h, (alt, neighbor))

    return dist, prev


def neighbors(current: (int, int), grid):
    x, y = current
    shape = grid.shape
    for i in[-1, 1]:
        k = x+i
        l = y
        if 0 <= k < shape[0] and 0 <= l < shape[1] and grid[k,l] != '#':
            yield k, l

        k = x
        l = y+i
        if 0 <= k < shape[0] and 0 <= l < shape[1] and grid[k,l] != '#':
            yield k, l


def distance(p1: (int, int), p2: (int, int)):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Day20(AbstractDay):
    def preprocess(self):
        grid = np.array([list(l) for l in self.puzzle])
        start = np.argwhere(grid == 'S')[0]
        self.start = (start[0].item(), start[1].item())
        end = np.argwhere(grid == 'E')[0]
        self.end = (end[0].item(), end[1].item())
        grid[*end] = '.'
        grid[*start] = '.'
        self.grid = grid

    def part1(self):
        grid = self.grid
        s = self.start
        e = self.end
        dist, prev = dijkstra(s, e, grid)
        path = []
        u = e
        while u in prev or u != s:
            path.append(u)
            u = prev[u]
        path.append(s)

        c1 = Counter()
        c2 = Counter()
        for i in range(len(path)):
            for j in range(i, len(path)):
                p1 = path[i]
                p2 = path[j]
                d = distance(p1, p2)
                if d == 2:
                    c1[j-i-d] += 1
                if d <= 20:
                    c2[j-i-d] += 1
        self.c2 = c2

        res = 0
        for k, v in c1.items():
            if k >= 100:
                res += v

        return res

    def part2(self):
        res = 0
        for k, v in self.c2.items():
            if k >= 100:
                res += v
            if k >= 50:
                #print(v, k)
                pass
        return res

