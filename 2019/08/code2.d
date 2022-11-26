import std.stdio;
import std.conv;

import std.range;
import std.string;
import std.algorithm;
import std.string;
import std.file;
import std.array;


void main()
{
  int[][] code = readText("input01.txt").strip.split("").map!(a =>
      to!int(a)).array.chunks(25*6).array;

  auto picture = code.fold!((a, b) => 
      a.zip(b).map!(c =>
        c[0]<2?c[0]:c[1]).array);

  picture.chunks(25).map!(a => 
      a.map!(x => x ? "O" : " ")).each!(a =>
      writeln(a.joiner));
}
