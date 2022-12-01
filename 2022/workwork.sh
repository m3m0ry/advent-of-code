#!/bin/sh
if [ $# != 1 ]; then
    echo "usage: sh workwork.sh <day>"
    echo "       day: 1-25 of Advent of Code Days"
    exit
fi

while true
do
    clear
    cargo run --manifest-path advent-of-code/Cargo.toml -- $1 ./inputs/day$1.txt || true
    inotifywait -e modify -q -r ./advent-of-code ./inputs
done
