import bisect
import itertools

from dataclasses import dataclass
from math import inf

from boiler import AbstractDay


@dataclass
class Mapping:
    destination: int
    source: int
    length: int


@dataclass
class Map:
    mappings: [Mapping]


def parse_input(puzzle):
    seeds = [int(i) for i in puzzle[0].split(':')[1].split()]
    mappings = []
    for k, g in itertools.groupby(puzzle[2:], lambda x: not x):
        if not k:
            mapy = []
            for mapping in itertools.islice(g, 1, None):
                destination, source, length = mapping.split()
                mapy.append(Mapping(int(destination), int(source), int(length)))
            mapy = sorted(mapy, key=lambda x: x.source)
            mappings.append(mapy)

    return seeds, mappings



# Python 3.12 itertools
def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(itertools.islice(it, n))):
        yield batch


class Day5(AbstractDay):
    def part1(self):
        seeds, mappings = parse_input(self.puzzle)
        seeds_dest = []
        for seed in seeds:
            dest = seed
            for mapping in mappings:
                bi = bisect.bisect(mapping, dest, key = lambda x: x.source)
                mapy = mapping[bi-1]
                if dest in range(mapy.source, mapy.source + mapy.length):
                    dest += mapy.destination - mapy.source
            seeds_dest.append(dest)
        return min(seeds_dest)


    def part2(self):
        seeds, mappings = parse_input(self.puzzle)
        new_seeds = []
        for start, length in batched(seeds, 2):
            new_seeds.append(range(start, start + length))
            
        seed_dest = inf
        for r in new_seeds:
            for seed in r:
                dest = seed
                for mapping in mappings:
                    bi = bisect.bisect(mapping, dest, key = lambda x: x.source)
                    mapy = mapping[bi-1]
                    if dest in range(mapy.source, mapy.source + mapy.length):
                        dest += mapy.destination - mapy.source
                seed_dest = min(seed_dest, dest)
        return seed_dest

