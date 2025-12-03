from boiler import AbstractDay

class Day3(AbstractDay):
    def preprocess(self):
        self.ints = [[int(d) for d in line] for line in self.puzzle]

    def part1(self):
        res = 0
        for bat in self.ints:
            index, first = max(enumerate(bat[:-1]), key=(lambda x: x[1]))
            second = max(bat[index+1:])
            res += first * 10 + second
        return res

    def part2(self):
        res = 0
        batteries = 12
        for bat in self.ints:
            numbers = []
            index = 0
            for i in range(batteries-1, -1, -1):
                if i == 0:
                    new_index, greatest = max(enumerate(bat[index:]), key=(lambda x: x[1]))
                else:
                    new_index, greatest = max(enumerate(bat[index:-i]), key=(lambda x: x[1]))
                index += 1 + new_index
                numbers.append(greatest)
            res += sum(10**i * n for i, n in enumerate(reversed(numbers)))
        return res

