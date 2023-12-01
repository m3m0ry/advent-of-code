import string

from collections import namedtuple
from math import inf

from boiler import AbstractDay

class Day1(AbstractDay):
    def part1(self):
        result = 0
        for x in self.puzzle:
            first = next(filter(lambda a: a in string.digits, x))
            last = next(filter(lambda a: a in string.digits, reversed(x)))
            result += int(first + last)
        return result

    def part2(self):
        numbers = {'1': '1',
                   '2': '2',
                   '3': '3',
                   '4': '4',
                   '5': '5',
                   '6': '6',
                   '7': '7',
                   '8': '8',
                   '9': '9',
                   'one': '1',
                   'two': '2',
                   'three': '3',
                   'four': '4',
                   'five': '5',
                   'six': '6',
                   'seven': '7',
                   'eight': '8',
                   'nine': '9',
                   }
        IndexedNumber = namedtuple('Number', ['index', 'value'], defaults=[inf, ''])

        result = 0

        for x in self.puzzle:
            first = IndexedNumber()
            for number in numbers:
                try:
                    index = x.index(number)
                    first = min(first, IndexedNumber(index, numbers[number]))
                except ValueError:
                    pass
            first = first.value

            xreversed = ''.join(reversed(x))
            last = IndexedNumber()
            for number in numbers:
                try:
                    index = xreversed.index(''.join(reversed(number)))
                    last = min(last, IndexedNumber(index, numbers[number]))
                except ValueError:
                    pass
            last = last.value

            result += int(first + last)
        return result

