from boiler import AbstractDay

import math

from collections import defaultdict
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
        if 0 <= k < shape[0] and 0 <= l < shape[1] and grid[k,l] != 'x': # TODO switch 0 and 1?
            yield k, l

        k = x
        l = y+i
        if 0 <= k < shape[0] and 0 <= l < shape[1] and grid[k,l] != 'x': # TODO switch 0 and 1?
            yield k, l

class Day18(AbstractDay):
    def preprocess(self):
        self.corrupted = []
        for p in self.puzzle:
            p = p.split(',')
            self.corrupted.append((int(p[1]), int(p[0])))

    def part1(self):
        cor = self.corrupted
        s = (0, 0)
        e = (70, 70)

        arr = np.full((71, 71), '.')
        for i in range(1024):
            arr[*cor[i]] = 'x'
        dist, prev = dijkstra((0, 0), (6, 6), arr)
        path = []
        u = e
        while u in prev or u != s:
            path.append(u)
            u = prev[u]
        #path.append(s)
        for p in path:
            arr[*p] = 'O'
        return (arr=='O').sum()

    def part2(self):
        cor = self.corrupted
        s = (0, 0)
        e = (70, 70)
        arr = np.full((71, 71), '.')

        dist, prev = dijkstra(s, e, arr)
        path = []
        u = e
        while u in prev or u != s:
            path.append(u)
            u = prev[u]

        for c in cor:
            arr[*c] = 'x'

            if c in path:
                dist, prev = dijkstra(s, e, arr)
                path = []
                u = e
                if u not in prev:
                    return f'{c[1]},{c[0]}'
                while u in prev or u != s:
                    path.append(u)
                    u = prev[u]

        return None

