import re
from dataclasses import dataclass
from functools import reduce

from boiler import AbstractDay

@dataclass
class Card:
    id: int
    winning: list[int]
    have: list[int]
    instances: int = 1


def parse_input(data) -> list[Card]:

    card_pattern = re.compile(r"Card\s+(\d+)")
    cards = []
    for line in data:
        card_part, rest = line.split(":")
        card_id = int(card_pattern.findall(card_part)[0])
        winning, have = rest.split("|")
        winning = [int(e) for e in winning.split()]
        have = [int(e) for e in have.split()]
        cards.append(Card(card_id, winning, have))
    return cards

class Day4(AbstractDay):
    def part1(self):
        cards = parse_input(self.puzzle)
        return sum(map(lambda x: 2**(x-1) if x >= 1 else 0, (sum(map(lambda x: 1 if x in card.winning else 0, card.have)) for card in cards)))

    def part2(self):
        cards = parse_input(self.puzzle)
        for i in range(len(cards)):
            card = cards[i]
            for j in range(1, 1+sum(map(lambda x: 1 if x in card.winning else 0, card.have))):
                cards[i+j].instances += card.instances
        return sum(map(lambda x: x.instances, cards))

