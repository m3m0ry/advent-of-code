from boiler import AbstractDay

from collections import Counter

def even(stone):
    return len(str(abs(stone))) % 2 == 0

def next_stone(stone):
    match stone:
        case 0:
            return [1]
        case stone if even(stone):
            stone_str = str(abs(stone))
            half = len(stone_str)//2
            return [int(stone_str[:half]) , int(stone_str[half:])]
        case _:
            return [stone*2024]


class Day11(AbstractDay):
    def preprocess(self):
        assert len(self.puzzle) == 1, 'Puzzle too long'
        self.stones = [int(i) for i in self.puzzle[0].split()]

    def part1(self):
        stones = self.stones
        new_stones = []
        blinks = 25
        for _ in range(blinks):
            for stone in stones:
                new_stones.extend(next_stone(stone))
            stones, new_stones = new_stones, []
        return len(stones)

    def part2(self):
        stones = Counter(self.stones)
        new_stones = stones.copy()
        blinks = 75
        for i in range(blinks):
            for stone in stones:
                new_stones[stone] -= stones[stone]
                for s in next_stone(stone):
                    new_stones[s] += stones[stone]
            stones = new_stones.copy()
        return stones.total()

