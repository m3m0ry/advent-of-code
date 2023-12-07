from collections import Counter
from dataclasses import dataclass

from boiler import AbstractDay


@dataclass
class Hand:
    cards: list[int]
    bid: int
    hand_type: int

def parse_input(puzzle):
    card_to_int = {str(i): i for i in range(2, 10)}
    card_to_int['T'] = 10
    card_to_int['J'] = 11
    card_to_int['Q'] = 12
    card_to_int['K'] = 13
    card_to_int['A'] = 14
    hands = []
    for line in puzzle:
        line = line.split()
        cards = [card_to_int[c] for c in line[0]]
        hands.append(Hand(cards, int(line[1]), hand_type(cards)))
    return hands

def hand_type(cards):
    counter = Counter(cards)
    most = counter.most_common()
    first = most[0][1]
    if first == 5:
        return 6
    elif first == 4:
        return 5
    elif first == 3 and most[1][1] == 2: # full house
        return 4
    elif first == 3:
        return 3
    elif first == 2 and most[1][1] == 2: # two pair
        return 2
    elif first == 2:
        return 1
    else:
        return 0

def camel_value(hand: Hand):
    return sum((card * i for card, i in zip(hand.cards, [100000000, 1000000, 10000, 100, 1]))) + hand.hand_type * 10000000000


def parse_input2(puzzle):
    card_to_int = {str(i): i for i in range(2, 10)}
    card_to_int['T'] = 10
    card_to_int['J'] = 1
    card_to_int['Q'] = 12
    card_to_int['K'] = 13
    card_to_int['A'] = 14
    hands = []
    for line in puzzle:
        line = line.split()
        cards = [card_to_int[c] for c in line[0]]
        hands.append(Hand(cards, int(line[1]), hand_type2(cards)))
    return hands

def hand_type2(cards):
    counter = Counter(cards)
    js = counter[1]
    if js == 5:
        return 6
    del counter[1]
    most = counter.most_common()
    first = most[0][1]
    if first == 5 - js:
        return 6
    elif first == 4 -js:
        return 5
    elif first == 3 -js and most[1][1] == 2: # full house
        return 4
    elif first == 3 - js:
        return 3
    elif first == 2 - js  and most[1][1] == 2: # two pair
        return 2
    elif first == 2 - js:
        return 1
    else:
        return 0

class Day7(AbstractDay):
    def part1(self):
        hands = parse_input(self.puzzle)
        sorted_hands = sorted(hands, key=camel_value)
        result = 0
        for i, hand in enumerate(sorted_hands, start=1):
            result += hand.bid * i
        return result



    def part2(self):
        hands = parse_input2(self.puzzle)
        sorted_hands = sorted(hands, key=camel_value)
        result = 0
        for i, hand in enumerate(sorted_hands, start=1):
            result += hand.bid * i
        return result

