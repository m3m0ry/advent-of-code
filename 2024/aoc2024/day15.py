from boiler import AbstractDay

import numpy as np


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
        grid = self.grid
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
        return None

