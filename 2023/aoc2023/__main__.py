import argparse
import importlib
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
            prog='AoC2023',
            description='Advent of Code solutions in Python for the year 2023')
    parser.add_argument('day', type=int, help='xth day as number')
    parser.add_argument('input_file', help='input file location for xth day puzzle')
    args = parser.parse_args()

    cur_dir = Path(__file__).parent
    day_path = Path(cur_dir / f'day{args.day}.py')
    if day_path.exists():
        lib = importlib.import_module(day_path.stem)
        day_cls = getattr(lib, f'Day{args.day}')
    else:
       raise NotImplementedError(f'Day {args.day} not yet implemented, run newday.sh!')

    with open(Path(args.input_file)) as f:
        input_text: [str] = f.readlines()

    day = day_cls(input_text)
    print(f'Day{args.day} Part 1: {day.part1()}')
    print(f'Day{args.day} Part 2: {day.part2()}')


if __name__ == '__main__':
    main()
