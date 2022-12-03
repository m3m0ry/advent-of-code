use std::collections::HashSet;

pub fn run(input: String) {
    let mut result: u32 = 0;
    for sac in input.lines().filter(|x| !x.is_empty()) {
        let left = sac[0..sac.len()/2].chars().collect::<Vec<_>>();
        let right = sac[sac.len()/2..].chars().collect::<Vec<_>>();
        let mut left_h = HashSet::new();
        let mut right_h = HashSet::new();
        right_h.extend(right);
        left_h.extend(left);
        let u: HashSet<_> = left_h.intersection(&right_h).collect();

        debug_assert!(u.len() == 1);
        result += score_item(**u.iter().next().unwrap()) as u32;
    }
    println!("Part1: {}", result);


    let mut result2: u32 = 0;
    for group in input.lines().filter(|x| !x.is_empty()).collect::<Vec<_>>().chunks(3) {
        let first: HashSet<char> = group[0].chars().collect();
        let second: HashSet<char> = group[1].chars().collect();
        let third: HashSet<char> = group[2].chars().collect();
        let u: HashSet<_> = first.intersection(&second).cloned().collect();
        let v: HashSet<_> = u.intersection(&third).collect();

        debug_assert!(v.len() == 1);
        result2 += score_item(**v.iter().next().unwrap()) as u32;
    }
    println!("Part2: {}", result2);
}

fn score_item(char_: char) -> u8 {
    match char_ as u8 {
        97..=122 => char_ as u8 - 96,
        65..=90 => char_ as u8 - 38,
        _ => unreachable!(),
    }
}
