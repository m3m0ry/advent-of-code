#!/bin/sh
if [ $# != 1 ]; then
    echo "usage: sh newday.sh <day>"
    echo "       day: 1-25 of Advent of Code Days"
    exit
fi

cp aoc2024/day0.py aoc2024/day$1.py
sed -i "s/0/$1/g" aoc2024/day$1.py
git add aoc2024/day$1.py

touch inputs/day$1.txt
#git add inputs/day$1.txt
