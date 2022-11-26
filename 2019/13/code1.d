import std.stdio;
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


alias Coord = Tuple!(BigInt, BigInt);


void main()
{
  immutable BigInt[] code = readText("input01.txt").strip.split(",").map!(a => to!BigInt(a)).array.assumeUnique;

  auto tid = spawnLinked(function(immutable BigInt[] input){Program(input, ownerTid).compute;
      }, code);

  bool[Coord] blocks;
  try {
    while (true) {
      //send(tid, painter.at ? BigInt(1) : BigInt(0));

      BigInt x, y, id;
      receive(((BigInt a) => x = a));
      receive(((BigInt a) => y = a));
      receive(((BigInt a) => id = a));
      if (id == 2.BigInt)
        blocks[Coord(x,y)] = true;
    }
  } catch (LinkTerminated e) { }
  writeln(blocks.length);
}

