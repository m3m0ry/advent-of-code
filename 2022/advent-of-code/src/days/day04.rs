
pub fn run(input: String) {
    let mut result: u32 = 0;
    let mut result2: u32 = 0;
    for (first, second) in input.lines().map(|x| x.split_once(',').unwrap()) {
        let mut range = first.split('-').map(|x| x.parse::<u32>().unwrap());
        let x_min = range.next().unwrap();
        let x_max = range.next().unwrap();
        let mut range2 = second.split('-').map(|x| x.parse::<u32>().unwrap());
        let y_min = range2.next().unwrap();
        let y_max = range2.next().unwrap();
        result += ((x_min <= y_min && x_max >= y_max) || (x_min >= y_min && x_max <= y_max)) as u32;
        result2 += (x_min.max(y_min) <= x_max.min(y_max)) as u32;
    }
    println!("Part1: {}", result);
    println!("Part2: {}", result2);
}