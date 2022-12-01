use itertools::*;

pub fn run(input: String) {
    let mut data_grouped: Vec<u32> = Vec::new();
    for (key, group) in &input.lines().group_by(|l| *l != "") {
        if key{
            data_grouped.push(group.fold(0u32, |sum, val| return sum + val.parse::<u32>().unwrap()));
        }
    }
    println!("Part1: {:?}", data_grouped.iter().max());
    println!("Part2: {:?}", data_grouped.iter().sorted().rev().take(3).sum::<u32>());
}
