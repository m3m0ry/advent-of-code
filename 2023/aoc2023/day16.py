from dataclasses import dataclass
from enum import StrEnum, auto, Flag

import numpy as np

from boiler import AbstractDay


class Was(Flag):
    NOT = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Is(StrEnum):
    SPACE = '.'
    HSPLITTER = '-'
    VSPLITTER = '|'
    UDMIRROR = '\\'
    DUMIRROR = '/'


@dataclass
class Step:
    x: int
    y: int
    direction: Was

    def left(self):
        return Step(self.x, self.y-1, self.direction)

    def right(self):
        return Step(self.x, self.y+1, self.direction)

    def up(self):
        return Step(self.x-1, self.y, self.direction)

    def down(self):
        return Step(self.x+1, self.y, self.direction)

    def __call__(self, grid):
        return grid[self.x, self.y]

def next_step(step, grid):
    match step.direction:
        case Was.UP:
            new = step.up()
        case Was.DOWN:
            new = step.down()
        case Was.LEFT:
            new = step.left()
        case Was.RIGHT:
            new = step.right()
        case _:
            assert false, 'WTF'
    return new


def parse_input(puzzle):
    return np.array([[c for c in line] for line in puzzle])


def beamsy(beams, grid):
    visited = np.full(grid.shape, Was.NOT)
    rows, cols = grid.shape
    while len(beams) != 0:
        beam = beams.pop()
        while True:
            beam = next_step(beam, grid)

            if beam.y < 0 or beam.x < 0 or beam.y >= cols or beam.x >= rows:
                break
            if beam.direction in visited[beam.x, beam.y]:
                break

            visited[beam.x, beam.y] |= beam.direction
            if beam.direction in (Was.LEFT | Was.RIGHT) and beam(grid) == Is.VSPLITTER:
                beam.direction = Was.UP
                beams.append(Step(beam.x, beam.y, Was.DOWN))
            elif beam.direction in (Was.UP | Was.DOWN) and beam(grid) == Is.HSPLITTER:
                beam.direction = Was.LEFT
                beams.append(Step(beam.x, beam.y, Was.RIGHT))
            elif beam(grid) == Is.UDMIRROR:
                match beam.direction:
                    case Was.UP:
                        beam.direction = Was.LEFT
                    case Was.DOWN:
                        beam.direction = Was.RIGHT
                    case Was.LEFT:
                        beam.direction = Was.UP
                    case Was.RIGHT:
                        beam.direction = Was.DOWN
            elif beam(grid) == Is.DUMIRROR:
                match beam.direction:
                    case Was.UP:
                        beam.direction = Was.RIGHT
                    case Was.DOWN:
                        beam.direction = Was.LEFT
                    case Was.LEFT:
                        beam.direction = Was.DOWN
                    case Was.RIGHT:
                        beam.direction = Was.UP
    return np.count_nonzero(visited != Was.NOT)


class Day16(AbstractDay):
    def part1(self):
        grid = parse_input(self.puzzle)
        beams = [Step(0, -1, Was.RIGHT)]
        return beamsy(beams, grid)

    def part2(self):
        grid = parse_input(self.puzzle)
        rows, cols = grid.shape
        result = 0
        for i in range(rows):
            beams = [Step(i,-1,Was.RIGHT)]
            result = max(result, beamsy(beams, grid))
            beams = [Step(i,cols,Was.LEFT)]
            result = max(result, beamsy(beams, grid))
        for j in range(cols):
            beams = [Step(-1,j,Was.DOWN)]
            result = max(result, beamsy(beams, grid))
            beams = [Step(rows,j,Was.UP)]
            result = max(result, beamsy(beams, grid))

        return result

