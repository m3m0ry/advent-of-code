import std.stdio;
import std.conv;

import std.range;
import std.string;
import std.algorithm;
import std.string;
import std.file;



void main()
{
  int[][] code = readText("input01.txt").strip.split("").map!(a =>
      to!int(a)).array.chunks(25*6).array;
  auto layer = code.minElement!"count(a,0)";
  writeln(layer.count(1) * layer.count(2));
}
