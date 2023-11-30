
class AbstractDay:

    def __init__(self, puzzle: [str]):
        self.puzzle = puzzle

    def _name(self):
        return self.__class__.__name__

    def part1(self):
        raise NotImplementedError(f'Part1 of day {self._name()} not yet implemented')

    def part2(self):
        raise NotImplementedError(f'Part1 of day {self._name()} not yet implemented')


