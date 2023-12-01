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
        numbers = {'one': '1',
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
            first_numeral = IndexedNumber()
            first_word = IndexedNumber()
            for number in numbers:
                try:
                    index = x.index(str(numbers[number]))
                    first_numeral = min(first_numeral, IndexedNumber(index, x[index]))
                except ValueError:
                    pass

                try:
                    index = x.index(number)
                    first_word = min(first_word, IndexedNumber(index, numbers[number]))
                except ValueError:
                    pass
            first = first_word.value if first_word < first_numeral else first_numeral.value

            xreversed = ''.join(reversed(x))
            last_numeral = IndexedNumber()
            last_word = IndexedNumber()
            for number in numbers:
                try:
                    index = xreversed.index(str(numbers[number]))
                    last_numeral = min(last_numeral, IndexedNumber(index, xreversed[index]))
                except ValueError:
                    pass

                try:
                    index = xreversed.index(''.join(reversed(number)))
                    last_word = min(last_word, IndexedNumber(index, numbers[number]))
                except ValueError:
                    pass
            last = last_word.value if last_word < last_numeral else last_numeral.value

            result += int(first + last)
        return result

