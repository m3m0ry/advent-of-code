import bisect

from boiler import AbstractDay

def parse_input1(puzzle):
    return [int(t) for t in puzzle[0].split(':')[1].split()], [int(t) for t in puzzle[1].split(':')[1].split()]

def parse_input2(puzzle):
    times, distances = [t.strip() for t in puzzle[0].split(':')[1].split()], [t.strip() for t in puzzle[1].split(':')[1].split()]
    return int(''.join(times)), int(''.join(distances))


class Day6(AbstractDay):
    def part1(self):
        times, distances = parse_input1(self.puzzle)
        result = 1
        for time, distance in zip(times, distances):
            number_of_ways = 0
            for t in range(0,time+1):
                if (time-t) * t > distance:
                    number_of_ways += 1
            result *= number_of_ways
        return result

    def part2(self):
        time, distance = parse_input2(self.puzzle)
        left = bisect.bisect(list(range(0, time+1)), distance, key = lambda t: (time - t) * t)
        right = bisect.bisect(list(range(time+1, 0, -1)), distance, key = lambda t: (time - t) * t)
        right = time + 2 - right
        print(left, right)
        return right - left

