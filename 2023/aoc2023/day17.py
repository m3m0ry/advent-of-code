import bisect
import heapq
from dataclasses import dataclass
from enum import StrEnum
import numpy as np
from boiler import AbstractDay

def parse_input(puzzle):
    return np.array([[int(c) for c in line] for line in puzzle])


class Dir(StrEnum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'
    NOT = '_'


@dataclass
class Step:
    x: int
    y: int
    straight_dir: Dir = Dir.NOT
    straight: int = 0
    dist: int = 0

    def left(self, grid):
        straight = self.straight+1 if self.straight_dir == Dir.LEFT else 1
        step = Step(self.x, self.y-1, Dir.LEFT, straight, self.dist)
        step.dist += step(grid)
        return step

    def right(self, grid):
        straight = self.straight+1 if self.straight_dir == Dir.RIGHT else 1
        step = Step(self.x, self.y+1, Dir.RIGHT, straight, self.dist)
        step.dist += step(grid)
        return step

    def up(self, grid):
        straight = self.straight+1 if self.straight_dir == Dir.UP else 1
        step = Step(self.x-1, self.y, Dir.UP, straight, self.dist)
        step.dist += step(grid)
        return step

    def down(self, grid):
        straight = self.straight+1 if self.straight_dir == Dir.DOWN else 1
        step = Step(self.x+1, self.y, Dir.DOWN, straight, self.dist)
        step.dist += step(grid)
        return step

    def __call__(self, grid):
        return grid[self.x, self.y]

    def __hash__(self):
        return hash(hash(self.x) + hash(self.y) + hash(self.straight_dir) + hash(self.straight))


def neighbors(current, grid, visited):
    n = [current.left(grid), current.right(grid), current.up(grid), current.down(grid)]
    rows, cols = grid.shape
    first = filter(lambda x: x.straight < 3, n)
    second = filter(lambda x: x not in visited, first)
    yield from filter(lambda x: x.x >= 0 and x.y >= 0 and x.x < rows and x.y < cols, second)


class Day17(AbstractDay):
    def part1(self):
        grid = parse_input(self.puzzle)
        rows, cols = grid.shape
        visited = set()
        Q = [Step(0, 0)]
        target = (rows-1, cols-1)
        while len(Q) != 0:
            u = Q.pop(0)
            for neighbor in neighbors(u, grid, visited):
                print(neighbor)

        return None

    def part2(self):
        return None

