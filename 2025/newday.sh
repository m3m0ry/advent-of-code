#!/bin/sh
if [ $# != 1 ]; then
    echo "usage: sh newday.sh <day>"
    echo "       day: 1-25 of Advent of Code Days"
    exit
fi

cp aoc2025/day0.py aoc2025/day$1.py
sed -i "s/0/$1/g" aoc2025/day$1.py
git add aoc2025/day$1.py

touch inputs/day$1.txt
