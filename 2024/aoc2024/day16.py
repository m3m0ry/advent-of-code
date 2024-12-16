from boiler import AbstractDay

import math

from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush

import numpy as np

@dataclass(eq=True, frozen=True, order=True)
class Node:
    position: (int, int)
    direction: str


def dijkstra(start, goal, grid):
    h = []
    heappush(h, (0, start))

    prev = dict()

    dist = defaultdict(lambda: math.inf)
    dist[start] = 0

    while h:
        current = heappop(h)[1]

        for neighbor, cost in neighbors(current, grid):
            alt = dist[current] + cost
            if alt < dist[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                prev[neighbor] = [current]
                dist[neighbor] = alt
                heappush(h, (alt, neighbor))
            elif alt == dist[neighbor]:
                # Equally good path
                prev[neighbor].append(current)

    return dist, prev


def neighbors(current: Node, grid):
    x, y = current.position
    match current.direction:
        case '<':
            if grid[x, y-1] == '.':
                yield Node((x, y-1), '<'), 1
            yield Node((x,y), '^'), 1000
            yield Node((x,y), 'v'), 1000
        case '>':
            if grid[x, y+1] == '.':
                yield Node((x, y+1), '>'), 1
            yield Node((x,y), '^'), 1000
            yield Node((x,y), 'v'), 1000
        case 'v':
            if grid[x+1, y] == '.':
                yield Node((x+1, y), 'v'), 1
            yield Node((x,y), '>'), 1000
            yield Node((x,y), '<'), 1000
        case '^':
            if grid[x-1, y] == '.':
                yield Node((x-1, y), '^'), 1
            yield Node((x,y), '>'), 1000
            yield Node((x,y), '<'), 1000

class Day16(AbstractDay):
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
        s = self.start
        e = self.end
        grid = self.grid
        start = Node(position = s, direction = '>')
        dist, prev = dijkstra(start, e, grid)
        path = []
        u = min((Node(e, s) for s in '<>^v'), key=lambda x: dist[x])
        while u in prev or u == s:
            path.append(u)
            u = prev[u]
            u = u[0]
        path.append(start)
        res = 0
        for step, prev_step in zip(path[1:], path):
            if step.direction != prev_step.direction:
                res += 1000
            else:
                res += 1
        return res

    def part2(self):
        s = self.start
        e = self.end
        grid = self.grid
        gp = grid.copy()
        start = Node(position = s, direction = '>')
        dist, prev = dijkstra(start, e, grid)
        path = []
        us = []
        m = min((dist[Node(e, s)] for s in '<>^v'))
        for n in (Node(e, s) for s in '<>^v'):
            if dist[n] == m:
                us.append(n)
        while us:
            u = us.pop()
            while u in prev or u == s:
                path.append(u)
                u = prev[u]
                if len(u) > 1:
                    us.extend(u[1:])
                u = u[0]
        path.append(start)
        for p in path:
            gp[*p.position] = 'O'
        return (gp=='O').sum()


