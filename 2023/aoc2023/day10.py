import itertools

import numpy as np

from dataclasses import dataclass

from boiler import AbstractDay



#    | is a vertical pipe connecting north and south.
#    - is a horizontal pipe connecting east and west.
#    L is a 90-degree bend connecting north and east.
#    J is a 90-degree bend connecting north and west.
#    7 is a 90-degree bend connecting south and west.
#    F is a 90-degree bend connecting south and east.
#    . is ground; there is no pipe in this tile.
#    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', '.')
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector


@dataclass
class Coord:
    x: int
    y: int

    def left(self):
        return Coord(self.x, self.y-1)

    def right(self):
        return Coord(self.x, self.y+1)

    def up(self):
        return Coord(self.x-1, self.y)

    def down(self):
        return Coord(self.x+1, self.y)

    def __call__(self, maze):
        return maze[self.x, self.y]

    def __sub__(self, o):
        return Coord(self.x - o.x, self.y - o.y)

    def __add__(self, o):
        return Coord(self.x + o.x, self.y + o.y)

    def __mul__(self, n):
        return Coord(self.x * n, self.y * n)

    def __truediv__(self, n):
        return Coord(self.x // n, self.y // n)



def next_direction(maze, coord, b4_coord):
    me = coord(maze)
    assert me != '.', f'Pipe broke here: {coord}'
    north = ['|', 'L', 'J', 'S']
    up = coord.up()
    south = ['|', '7', 'F', 'S']
    down = coord.down()
    east = ['-', 'L', 'F', 'S']
    right = coord.right()
    west = ['-', 'J', '7', 'S']
    left = coord.left()

    if me in north and up != b4_coord and up(maze) in south:
        return up
    if me in south and down != b4_coord and down(maze) in north:
        return down
    if me in east and right != b4_coord and right(maze) in west:
        return right
    if me in west and left != b4_coord and left(maze) in east:
        return left
    assert False, 'WTF'


class Day10(AbstractDay):
    def part1(self):
        maze = puzzle = np.array([list(s) for s in self.puzzle]) 
        maze = np.pad(maze, 1, pad_with, padder='.')
        xs, ys = np.where(maze == 'S')
        assert len(xs) == len(ys) == 1
        s = Coord(xs[0], ys[0])
        b4 = s
        steps = 0
        while True:
            steps += 1
            new_s = next_direction(maze, s, b4)
            s, b4 = new_s, s
            if s(maze) == 'S':
                break
        return steps // 2

    def part2(self):
        maze = puzzle = np.array([list(s) for s in self.puzzle]) 
        maze = np.pad(maze, 1, pad_with, padder='.')
        xs, ys = np.where(maze == 'S')
        assert len(xs) == len(ys) == 1
        s = Coord(xs[0], ys[0])
        b4 = s
        loop = np.zeros_like(maze, dtype = np.integer)
        steps = []
        while True:
            loop[s.x, s.y] = 1
            steps.append(s)
            new_s = next_direction(maze, s, b4)
            s, b4 = new_s, s
            if s(maze) == 'S':
                break

        rows, cols = loop.shape
        doubled = np.zeros((2 * rows -1, 2 * cols -1), dtype=loop.dtype)
        doubled[::2, ::2] = loop

        for f, t in zip(steps, itertools.chain(steps[1:], steps[:1])):
            f *= 2
            t *= 2
            fill_coord = (t-f)/2 + f
            doubled[fill_coord.x, fill_coord.y] = 1

        boundary_value = 2
        doubled[0, :] = boundary_value
        doubled[-1, :] = boundary_value

        # Assign to the left and right columns
        doubled[:, 0] = boundary_value
        doubled[:, -1] = boundary_value


        other = doubled.copy()
        while True:
            doubled = other.copy()
            rows, cols = doubled.shape
            # ugly, use pystencils
            for i in range(1, rows-1):
                for j in range(1, cols-1):
                    if doubled[i,j] != 1 and (doubled[i+1,j] == 2 or doubled[i-1,j] == 2 or doubled[i,j+1] == 2 or doubled[i,j-1] == 2):
                        other[i,j] = 2
            if np.array_equal(other, doubled):
                break


        back = np.zeros_like(loop)
        back = doubled[::2, ::2]

        return np.count_nonzero(back == 0)

