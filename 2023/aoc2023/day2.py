import re

from dataclasses import dataclass
from functools import reduce
from boiler import AbstractDay

@dataclass
class Sample:
    red: int=0
    blue: int=0
    green: int=0

@dataclass
class Game:
    id: int
    samples: list[Sample]

def parse_input(data) -> list[Game]:
    game_pattern = re.compile(r"Game\s+(\d+)")
    sample_pattern = re.compile(r"(\d+)\s*(\w+)")
    
    games = []
    for line in data:
        game_part, samples_part = line.split(":")
        game_id = int(game_pattern.findall(game_part)[0])
        samples = samples_part.split(";")
        
        game_samples = []
        for sample in samples:
            matches = sample_pattern.finditer(sample.strip())
            counts = {"red": 0, "green": 0, "blue": 0}
            for match in matches:
                count, colour = match.groups()
                counts[colour] = int(count)
            
            game_samples.append(Sample(counts["red"], counts["blue"], counts["green"]))
        
        games.append(Game(game_id, game_samples))
        
    return games

class Day2(AbstractDay):


    def part1(self):
        max_red = 12
        max_green =  13
        max_blue = 14
        self.games = parse_input(self.puzzle)

        valid_sample = lambda sample: sample.red <= max_red and sample.green <= max_green and sample.blue <= max_blue
        valid_game = lambda game: all((valid_sample(sample) for sample in game.samples))
        return reduce(lambda x, y: x + y.id, filter(valid_game, self.games), 0)

    def part2(self):
        # parsed in part1 into self.games
        max_color = lambda x, y: Sample(x.red if x.red > y.red else y.red, x.blue if x.blue > y.blue else y.blue, x.green if x.green > y.green else y.green)
        return reduce(lambda x, y: x + y.green * y.blue * y.red, (reduce(max_color, game.samples) for game in self.games), 0)

