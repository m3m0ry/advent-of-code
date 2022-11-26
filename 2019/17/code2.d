import std.stdio;
import std.random;
import std.file : readText;
import std.conv;
import std.range;
import std.algorithm;
import std.string;
import std.exception;
import std.container;
import std.bigint;
import std.traits;
import std.concurrency;
import std.typecons;

import machine;


void main()
{
  BigInt[] code = readText("input01.txt").strip.split(",").map!(a => to!BigInt(a)).array;
  code[0] = 2.BigInt;

  auto tid = spawnLinked(function(immutable BigInt[] input){Program(input, ownerTid).compute;
      }, code.assumeUnique);

  string picture;
  try {
    while (true) {
      receive((BigInt i) {picture ~= i.to!int.to!char;});
    }
  } catch (LinkTerminated e) { }
  writeln(picture);
  char[][] p = new char[][](picture.split.length, 0);
  foreach(i, line; picture.split.enumerate)
  {
    foreach(c; line.split(""))
    {
      p[i] ~= c;
    }
  }
  int counting;
  foreach(i; 1..p.length-1)
  {
    foreach(j; 1..p[i].length-1)
    {
      if(p[i][j] == '#' && p[i][j+1] == '#' && p[i][j-1] == '#' && p[i+1][j] == '#' && p[i-1][j] == '#')
      {
        counting += i*j;
      }
    }
  }
  writeln(counting);
}

