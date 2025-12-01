from boiler import AbstractDay


def turn(old_dial, rotation):
    rot = int(rotation[1:])
    num = -rot if rotation[0] == 'L' else rot
    dial = (old_dial + num) % 100

    click = abs(old_dial + num) // 100

    click += old_dial + num <= 0 and old_dial != 0

    return dial, click


class Day1(AbstractDay):
    def preprocess(self):
        return

    def part1(self):
        res = 0
        dial = 50
        for l in self.puzzle:
            dial, _ = turn(dial, l)
            if dial == 0:
                res += 1
        return res

    def part2(self):
        dial = 50
        clicks = 0
        for l in self.puzzle:
            dial, click = turn(dial, l)
            clicks += click
        return clicks

