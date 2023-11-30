#!/bin/sh
if [ $# != 1 ]; then
    echo "usage: sh workwork.sh <day>"
    echo "       day: 1-25 of Advent of Code Days"
    exit
fi

while true
do
    clear
    python aoc2023 -- $1 ./inputs/day$1.txt || true
    inotifywait -e modify -q -r ./aoc2023 ./inputs
done
