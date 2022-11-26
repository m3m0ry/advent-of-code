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


enum Direction{ Up, Down, Left, Right }

struct Painter{
  BigInt x, y;
  Direction dir;

  bool[Tuple!(BigInt, BigInt)] painted;

  bool at()
  {
    return (tuple(x,y) in painted && painted[tuple(x,y)]);
  }

  void move(bool white, bool turnRight)
  {
    writeln("Painter(", x, ",", y, ") painting ", (white ? "white" : "black"), " turning ", (turnRight ? "right" : "left"));
    painted[tuple(x, y)] = white;
    //hull[tuple(x, y)] = white;
    if (turnRight) {
      final switch (dir) {
        case Direction.Up: dir = Direction.Right; break;
        case Direction.Down: dir = Direction.Left; break;
        case Direction.Left: dir = Direction.Up; break;
        case Direction.Right: dir = Direction.Down; break;
      }
    } else {
      final switch (dir) {
        case Direction.Up: dir = Direction.Left; break;
        case Direction.Down: dir = Direction.Right; break;
        case Direction.Left: dir = Direction.Down; break;
        case Direction.Right: dir = Direction.Up; break;
      }
    }
    final switch (dir) {
      case Direction.Up: --y; break;
      case Direction.Down: ++y; break;
      case Direction.Left: --x; break;
      case Direction.Right: ++x; break;
    }
  }
}



void main()
{
  immutable BigInt[] code = readText("input01.txt").strip.split(",").map!(a => to!BigInt(a)).array.assumeUnique;

  auto tid = spawnLinked(function(immutable BigInt[] input){Program(input, ownerTid).compute;
      }, code);

  auto painter = Painter();

  try {
    while (true) {
      send(tid, painter.at ? BigInt(1) : BigInt(0));
      bool white, turnRight;
      receive((BigInt i) { if (i > 0) white = true; });
      receive((BigInt i) { if (i > 0) turnRight = true; });
      painter.move(white, turnRight);
    }
  } catch (LinkTerminated e) { }
  writeln(painter.painted.length);
}

