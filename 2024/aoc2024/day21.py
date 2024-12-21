from boiler import AbstractDay

from functools import cache

import numpy as np


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


def paths(current, to, grid):
    if current == to:
        return ['']

    possible = []
    for neighbor in neighbors(current, grid):
        if distance(current, to) > distance(neighbor, to):
            # right path
            sub_paths = paths(neighbor, to, grid)
            for sub_path in sub_paths:
                possible.append(movement(current, neighbor) + sub_path)
    return possible


def distance(p1: (int, int), p2: (int, int)):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def movement(f: (int, int), t: (int, int)):
    if f[0] < t[0]:
        return 'v'
    elif f[0] > t[0]:
        return '^'
    elif f[1] < t[1]:
        return '>'
    elif f[1] > t[1]:
        return '<'
    else:
        raise NotImplementedError('No such neighbor path')


def shortest_paths(f, t, grid):
    moves = paths(f, t, grid)
    min_length = min(len(lst) for lst in moves)
    shortests = [lst + 'A' for lst in moves if len(lst) == min_length]
    return shortests


def robot(passcode, grid1, grid1_map, grid2, grid2_map, n, n_max):
    @cache
    def robotbot(passcode, n):
        if n == n_max+1:
            return len(passcode)
        grid = grid1 if n == 0 else grid2
        grid_map = grid1_map if n == 0 else grid2_map

        res = 0
        for f1, t1 in zip('A' + passcode, passcode):
            shortests = shortest_paths(grid_map[f1], grid_map[t1], grid)
            r = min((robotbot(shortest, n+1) for shortest in shortests))
            res += r
        return res
    return robotbot(passcode, n)


class Day21(AbstractDay):
    def preprocess(self):
        return

    def part1(self):
        passcodes = self.puzzle
        grid1 = np.array([['7', '8', '9'],['4', '5', '6'],['1', '2', '3'], ['#', '0', 'A']])
        grid1_map = {'7': (0,0),
                     '8': (0,1),
                     '9': (0,2),
                     '4': (1,0),
                     '5': (1,1),
                     '6': (1,2),
                     '1': (2,0),
                     '2': (2,1),
                     '3': (2,2),
                     '#': (3,0),
                     '0': (3,1),
                     'A': (3,2)}
        grid2 = np.array([['#', '^', 'A'],['<', 'v', '>']])
        grid2_map = {'#': (0,0),
                     '^': (0,1),
                     'A': (0,2),
                     '<': (1,0),
                     'v': (1,1),
                     '>': (1,2)}

        res = 0
        for passcode in passcodes:
            r = robot(passcode, grid1, grid1_map, grid2, grid2_map, 0, 2)
            res += int(passcode[:-1]) * r

        return res

    def part2(self):
        passcodes = self.puzzle
        grid1 = np.array([['7', '8', '9'],['4', '5', '6'],['1', '2', '3'], ['#', '0', 'A']])
        grid1_map = {'7': (0,0),
                     '8': (0,1),
                     '9': (0,2),
                     '4': (1,0),
                     '5': (1,1),
                     '6': (1,2),
                     '1': (2,0),
                     '2': (2,1),
                     '3': (2,2),
                     '#': (3,0),
                     '0': (3,1),
                     'A': (3,2)}
        grid2 = np.array([['#', '^', 'A'],['<', 'v', '>']])
        grid2_map = {'#': (0,0),
                     '^': (0,1),
                     'A': (0,2),
                     '<': (1,0),
                     'v': (1,1),
                     '>': (1,2)}

        res = 0
        for passcode in passcodes:
            r = robot(passcode, grid1, grid1_map, grid2, grid2_map, 0, 25)
            res += int(passcode[:-1]) * r

        return res


