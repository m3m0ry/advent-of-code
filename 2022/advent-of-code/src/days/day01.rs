use itertools::*;

pub fn run(input: String) {
    let mut data_grouped: Vec<u32> = Vec::new();
    for (key, group) in &input.lines().group_by(|l| !l.is_empty() ) {
        if key{
            data_grouped.push(group.flat_map(|c| c.parse::<u32>()).sum());
        }
    }
    println!("Part1: {:?}", data_grouped.iter().max().unwrap_or(&0));
    println!("Part2: {:?}", data_grouped.iter().sorted().rev().take(3).sum::<u32>());
}
