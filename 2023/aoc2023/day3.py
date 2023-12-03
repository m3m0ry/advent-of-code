import numpy as np

from collections import defaultdict
from math import prod

from boiler import AbstractDay

def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', '.')
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector


def adjacent_to(a, f):
    special = np.vectorize(f)(a)

    adjecent_to_special = np.full(special.shape, False)
    for i in range(-1, 2):
        for j in range(-1, 2):
            adjecent_to_special = np.logical_or(adjecent_to_special, np.roll(special, shift=(i, j), axis=(0,1)))
    return adjecent_to_special


def number_collective(a):
    number_ids = np.full(a.shape, -1)
    number_id = 0
    was_number = False
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if np.char.isnumeric(a[i,j]):
                number_ids[i,j] = number_id
                was_number = True
            elif was_number:
                number_id += 1
                was_number = False
    return number_ids



class Day3(AbstractDay):
    def part1(self):
        puzzle = np.array([list(s) for s in self.puzzle]) 
        padded = np.pad(puzzle, 1, pad_with, padder='.')

        number_ids = number_collective(padded)
        adjecent_to_symbol = adjacent_to(padded, lambda x: not x == '.' and not np.char.isnumeric(x) )
        relevant = np.copy(number_ids)
        relevant[~adjecent_to_symbol] = -1
        relevant_ids = set(np.unique(relevant))
        relevant_ids.discard(-1)

        numbers = defaultdict(list)
        for i in range(padded.shape[0]):
            for j in range(padded.shape[1]):
                if number_ids[i,j] in relevant_ids:
                    numbers[number_ids[i,j]].append(padded[i,j])

        return sum((int(''.join(number)) for number in numbers.values()))

    def part2(self):
        puzzle = np.array([list(s) for s in self.puzzle]) 
        padded = np.pad(puzzle, 1, pad_with, padder='.')
        number_mask = number_collective(padded)

        is_star = padded == '*'
        gears = []
        xs, ys = np.where(is_star)
        for x,y in zip(xs, ys):
            ids = set()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    current_id = number_mask[x+i, y+j]
                    if current_id != -1:
                        ids.add(current_id)
            gears.append(ids)
        gears = [gear for gear in gears if len(gear) == 2]
        numbers = defaultdict(list)
        for i in range(padded.shape[0]):
            for j in range(padded.shape[1]):
                numbers[number_mask[i,j]].append(padded[i,j])

        return sum((prod((int(''.join(numbers[i])) for i in gear)) for gear in gears))






