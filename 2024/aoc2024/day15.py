from boiler import AbstractDay

import numpy as np


class Unmovable(Exception):
    def __init__(self, message):
        super().__init__(message)


def first_space(grid, pos, dir):
    x, y = pos
    match dir:
        case '<':
            sub = np.flip(grid[x, :y])
            w = np.argwhere(sub == '.')
            wall = np.argwhere(sub == '#')
            if len(w):
                w = w[0].item()
                if w < wall[0]:
                    return x, y - w - 1
        case '>':
            sub = grid[x, y+1:]
            w = np.argwhere(sub == '.')
            wall = np.argwhere(sub == '#')
            if len(w):
                w = w[0].item()
                if w < wall[0]:
                    return x, y + w + 1
        case 'v':
            sub = grid[x+1:, y]
            w = np.argwhere(sub == '.')
            wall = np.argwhere(sub == '#')
            if len(w):
                w = w[0].item()
                if w < wall[0]:
                    return x + w + 1, y
        case '^':
            sub = np.flip(grid[:x, y])
            w = np.argwhere(sub == '.')
            wall = np.argwhere(sub == '#')
            if len(w):
                w = w[0].item()
                if w < wall[0]:
                    return x - w - 1, y
    return None

def mov_robot(pos, dir):
    x, y = pos
    match dir:
        case '<':
            return x, y-1
        case '>':
            return x, y+1
        case 'v':
            return x+1, y
        case '^':
            return x-1, y


def opposit_dir(dir):
    match dir:
        case '<':
            return '>'
        case '>':
            return '<'
        case 'v':
            return '^'
        case '^':
            return 'v'


class Day15(AbstractDay):
    def preprocess(self):
        for i, l in enumerate(self.puzzle):
            if not l:
                x = i
                break
        
        self.grid = np.array([list(l) for l in self.puzzle[0:x]])
        self.movements = ''.join(self.puzzle[i:])
        robot = np.argwhere(self.grid == '@')[0]
        self.robot = (robot[0].item(), robot[1].item())
        self.grid[*self.robot] = '.'


    def part1(self):
        grid = self.grid.copy()
        mov = self.movements
        pos = self.robot
        for m in mov:
            if (space := first_space(grid, pos, m)):
                k, l = space
                x, y = pos
                if x == k:
                    if y > l:
                        grid[x, l:y] = grid[x, l+1:y+1]
                        grid[*pos] = '.'
                    else:
                        grid[x, y+1:l+1] = grid[x, y:l]
                        grid[*pos] = '.'
                elif l == y:
                    if x > k:
                        grid[k:x, l] = grid[k+1:x+1, l]
                        grid[*pos] = '.'
                    else:
                        grid[x+1:k+1, l] = grid[x:k, l]
                        grid[*pos] = '.'

                pos = mov_robot(pos, m)

        res = 0
        crates = np.argwhere(grid == 'O')
        for crate in crates:
            res += 100 * crate[0] + crate[1]

        return res

    def part2(self):
        mov = self.movements

        shape = self.grid.shape
        grid = np.full((shape[0], shape[1]*2), '.')
        grid[:, ::2] = self.grid
        boxes = np.argwhere(grid == 'O')
        for i,j in boxes:
            grid[i,j] = '['
            grid[i,j+1] = ']'

        shape = grid.shape
        walls = np.argwhere(grid == '#')
        for i,j in walls:
            grid[i,j+1] = '#'


        pos = (self.robot[0], self.robot[1]*2)

        grid[*pos] = '@'
        for m in mov:
            if m in '<>':
                if (space := first_space(grid, pos, m)):
                    k, l = space
                    x, y = pos
                    if x == k:
                        if y > l:
                            grid[x, l:y] = grid[x, l+1:y+1]
                            grid[*pos] = '.'
                        else:
                            grid[x, y+1:l+1] = grid[x, y:l]
                            grid[*pos] = '.'
                    elif l == y:
                        if x > k:
                            grid[k:x, l] = grid[k+1:x+1, l]
                            grid[*pos] = '.'
                        else:
                            grid[x+1:k+1, l] = grid[x:k, l]
                            grid[*pos] = '.'

                    pos = mov_robot(pos, m)
            else: # 'v^'
                try:
                    to_move = find_boxes(grid, mov_robot(pos, m), m)
                    to_move.add(pos)
                    old = grid.copy()
                    for move in to_move:
                        grid[*move] = '.'
                    for move in to_move:
                        grid[*mov_robot(move, m)] = old[*move]
                    grid[*pos] = '.'

                    pos = mov_robot(pos, m)

                except Unmovable as _:
                    pass

        res = 0
        crates = np.argwhere(grid == '[')
        for crate in crates:
            res += 100 * crate[0] + crate[1]

        return res

def find_boxes(grid, pos, m):
    if grid[*pos] == '[':
        side = mov_robot(pos, '>')
        box = {pos, side}
        box |= find_boxes(grid, mov_robot(pos, m), m)
        box |= find_boxes(grid, mov_robot(side, m), m)
        return box
    elif grid[*pos] == ']':
        side = mov_robot(pos, '<')
        box = {pos, side}
        box |= find_boxes(grid, mov_robot(pos, m), m)
        box |= find_boxes(grid, mov_robot(side, m), m)
        return box
    elif grid[*pos] == '.':
        return set()
    else:
        raise Unmovable('No space to push into')
