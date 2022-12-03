#[derive(Clone, Copy, PartialEq)]
enum Move {
    Rock,
    Paper,
    Scissors,
}

impl Move {
    fn from_str(s: &str) -> Self {
        match s {
            "A" | "X" => Move::Rock,
            "B" | "Y" => Move::Paper,
            "C" | "Z" => Move::Scissors,
            _ => unreachable!(),
        }
    }
}

enum Outcome {
    Win,
    Lose,
    Tie,
}

impl Outcome {
    fn from_game(a: Move, b: Move) -> Outcome {
        if a == b {
            return Outcome::Tie;
        }
        if b == win(a) {
            return Outcome::Win;
        }
        Outcome::Lose
    }
    fn to_score(&self) -> u32 {
        match self {
            Outcome::Lose => 0,
            Outcome::Tie => 3,
            Outcome::Win => 6,
        }
    }
}

fn win(elf: Move) -> Move {
    match elf {
        Move::Rock => Move::Paper,
        Move::Paper => Move::Scissors,
        Move::Scissors => Move::Rock,
    }
}

fn lose(elf: Move) -> Move {
    match elf {
        Move::Rock => Move::Scissors,
        Move::Paper => Move::Rock,
        Move::Scissors => Move::Paper,
    }
}

fn strategy(elf: Move, me: &str) -> Move {
    match me {
        "X" => lose(elf),
        "Y" => elf,
        "Z" => win(elf),
        _ => elf,
    }
}

pub fn run(input: String) {
    //Part1
    let mut part1: u32 = 0;
    let mut part2: u32 = 0;
    for (elf, me) in input.lines().filter(|x| !x.is_empty()).map(|x| x.split_once(' ').unwrap()) {
        let me_move = Move::from_str(me);
        let elf_move = Move::from_str(elf);
        part1 += Outcome::from_game(elf_move, me_move).to_score();
        part1 += me_move as u32 + 1;
        let me_move2 = strategy(elf_move, me);
        part2 += Outcome::from_game(elf_move, me_move2).to_score();
        part2 += me_move2 as u32 + 1;
    }
    println!("Part1: {}", part1);
    println!("Part2: {}", part2);
}