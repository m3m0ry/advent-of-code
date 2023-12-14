import numpy as np
from tqdm import tqdm

from boiler import AbstractDay

def parse_input(puzzle):
    rocks = np.array([list(l) for l in puzzle])
    return rocks

def roll_north(rocks):
    rows, cols = rocks.shape
    for i in range(1, rows):
        for j in range(cols):
            if rocks[i,j] == 'O':
                k = i
                while k > 0 and rocks[k-1,j] == '.':
                    k -= 1
                if i != k:
                    rocks[k,j] = 'O'
                    rocks[i,j] = '.'
    return rocks


def roll_south(rocks):
    rows, cols = rocks.shape
    for i in reversed(range(rows-1)):
        for j in range(cols):
            if rocks[i,j] == 'O':
                k = i
                while k < rows-1 and rocks[k+1,j] == '.':
                    k += 1
                if i != k:
                    rocks[k,j] = 'O'
                    rocks[i,j] = '.'
    return rocks


def roll_west(rocks):
    rows, cols = rocks.shape
    for j in range(1, cols):
        for i in range(rows):
            if rocks[i,j] == 'O':
                k = j
                while k > 0 and rocks[i,k-1] == '.':
                    k -= 1
                if j != k:
                    rocks[i,k] = 'O'
                    rocks[i,j] = '.'
    return rocks


def roll_east(rocks):
    rows, cols = rocks.shape
    for j in reversed(range(cols-1)):
        for i in range(rows):
            if rocks[i,j] == 'O':
                k = j
                while k < cols-1 and rocks[i,k+1] == '.':
                    k += 1
                if j != k:
                    rocks[i,k] = 'O'
                    rocks[i,j] = '.'
    return rocks

def calculate(rocks):
    result = 0
    for i, row in enumerate(rocks):
        result += (len(row)-i)*np.sum(row == 'O')
    return result


class Day14(AbstractDay):
    def part1(self):
        rocks = parse_input(self.puzzle)
        rocks = roll_north(rocks)
        return calculate(rocks)



    def part2(self):
        rocks = parse_input(self.puzzle)
        already_there = [rocks.copy()]
        n = 1000000000
        for done in tqdm(range(1, n)):
            rocks = roll_north(rocks)
            rocks = roll_west(rocks)
            rocks = roll_south(rocks)
            rocks = roll_east(rocks)
            if any((np.array_equal(a, rocks) for a in already_there)):
                break
            already_there.append(rocks.copy())

        for index, a in enumerate(already_there):
            if np.array_equal(a, rocks):
                break

        cycle = done - index
        for cycle in tqdm(range((n-done) % cycle)):
            rocks = roll_north(rocks)
            rocks = roll_west(rocks)
            rocks = roll_south(rocks)
            rocks = roll_east(rocks)

        return calculate(rocks)

