from boiler import AbstractDay

from enum import Enum, auto

import numpy as np


class Dir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

def dir_to_string(dir):
    match dir:
        case Dir.UP:
            return 'U'
        case Dir.DOWN:
            return 'D'
        case Dir.LEFT:
            return 'L'
        case Dir.RIGHT:
            return 'R'

def turn(dir):
    match dir:
        case Dir.UP:
            return Dir.RIGHT
        case Dir.DOWN:
            return Dir.LEFT
        case Dir.LEFT:
            return Dir.UP
        case Dir.RIGHT:
            return Dir.DOWN


def sub(i, j, grid, dir):
    match dir:
        case Dir.UP:
            return grid[0:i, j]
        case Dir.DOWN:
            return grid[i+1:, j]
        case Dir.LEFT:
            return grid[i, 0:j]
        case Dir.RIGHT:
            return grid[i, j+1:]

def step(i,j, dir):
    match dir:
        case Dir.UP:
            return i-1, j
        case Dir.DOWN:
            return i+1, j
        case Dir.LEFT:
            return i, j-1
        case Dir.RIGHT:
            return i, j+1


def could_obstacle(i, j, grid, dir):
    k, l = step(i,j,dir)
    if grid[k,l] != '#' and grid[k,l] != '+' and grid[k,l] != '^':
        # could place an obstacle
        m, n  = step(i, j, turn(dir))
        if grid[m,n] == dir_to_string(turn(dir)):
            g = grid.copy()
            g[k,l] = 'O'
            print(g)
            # should create a loop
            return 1
    return 0


def loopforward2(i,j, grid, dir):
    obstacles = 0
    while True:
        obstacles += could_obstacle(i,j,grid,dir)
        i, j = step(i, j, dir)
        if grid[i,j] == '#':
            return i, j, False, obstacles
        if grid[i,j] == '+':
            return i, j, True, obstacles


def loopforward(i,j, grid, dir):
    while True:
        i, j = step(i, j, dir)
        if grid[i,j] == '#':
            return i, j, False
        if grid[i,j] == '+':
            return i, j, True


class Day6(AbstractDay):
    def preprocess(self):
        self.g = np.array([list(s) for s in self.puzzle])
        self.grid = np.array([list(s) for s in self.puzzle], dtype=object)

    def part1(self):
        grid = np.pad(self.g, 1, constant_values=('+'))
        i,j = np.argwhere(grid == '^')[0]
        o = Dir.UP
        out = False
        while not out:
            k, l, out = loopforward(i, j, grid, o)
            if k == i:
                grid[i, j:l:1 if j < l else -1] = 'X'
                if l < j:
                    j = l + 1
                else:
                    j = l -1
            else:
                grid[i:k:1 if i< k else -1, j] = 'X'
                if k < i:
                    i = k + 1
                else:
                    i = k -1
            o = turn(o)
        return np.count_nonzero(grid == 'X')

    def part2(self):
        grid = np.pad(self.grid, 1, constant_values=('+'))
        print(grid)
        i,j = np.argwhere(grid == '^')[0]
        o = Dir.UP
        out = False
        obstacles = 0
        while not out:
            k, l, out, obst = loopforward2(i, j, grid, o)
            obstacles += obst
            if k == i:
                grid[i, j:l:1 if j < l else -1] = grid[i, j:l:1 if j < l else -1] + dir_to_string(o)
                print(grid[i, j:l:1 if j < l else -1] + dir_to_string(o))
                print(grid[i, j:l:1 if j < l else -1])
                if l < j:
                    j = l + 1
                else:
                    j = l -1
            else:
                grid[i:k:1 if i< k else -1, j] += dir_to_string(o)
                if k < i:
                    i = k + 1
                else:
                    i = k -1
            o = turn(o)
        print(grid)
        return obstacles

