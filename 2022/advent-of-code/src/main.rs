mod days;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    println!("{:?}", args);
    if args.len() != 3 {
        eprintln!("error: invalid number of arguments");
        return;
    }

    let file = &args[2];
    let input = std::fs::read_to_string(file).expect("Could not read file!");
    let num = &args[1];
    let day: u32 = match num.parse() {
        Ok(n) => {
            n
        },
        Err(_) => {
            eprintln!("Could not parse day");
            return;
        }
    };

    match day {
        1 => days::day01::run(input),
        2 => days::day02::run(input),
        3 => days::day03::run(input),
        4 => days::day04::run(input),
        _ => {
            eprintln!("Day not yet defined");
        }
    }
}
