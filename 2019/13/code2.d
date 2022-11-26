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
  BigInt[] code = readText("input01.txt").strip.split(",").map!(a => to!BigInt(a)).array;
  code[0] = 2.BigInt;

  auto tid = spawnLinked(function(immutable BigInt[] input){Program(input, ownerTid).compute;
      }, code.assumeUnique);

  BigInt x, y, id, score;
  Coord paddle, ball;
  BigInt[Coord] game;
  try {
    while (true) {
      receive(((BigInt a) => x = a));
      receive(((BigInt a) => y = a));
      receive(((BigInt a) => id = a));
      game[Coord(x,y)] = id;
      if(id == 3.BigInt)
        paddle = Coord(x,y);
      else if(id == 4.BigInt)
        ball = Coord(x,y);
      else if(x == -1.BigInt)
      {
        writeln("Score: ", score);
        score = id;
      }
      else if(x == -2.BigInt)
      {
        if(ball[0] < paddle[0])
          send(tid, -1.BigInt);
        else if(ball[0] > paddle[0])
          send(tid, 1.BigInt);
        else
          send(tid, 0.BigInt);
      }

    }
  } catch (LinkTerminated e) { }
  writeln("Score: ", score);
}

