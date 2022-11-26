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

enum Direction{ North=1, South=2, West=3, East=4}
enum Status{ Wall=0, Move=1, Ox=2}
enum Karte{Unknown=0, Nothing=1, Wall=2, Ox=3}

string texture(Karte s)
{
  final switch(s)
  {
    case(Karte.Unknown): return " ";
    case(Karte.Nothing): return ".";
    case(Karte.Wall): return "#";
    case(Karte.Ox): return "X";
  }
}

void show(Karte[][] scout, Bot bot)
{
  foreach(i, row; scout.enumerate)
  {
    foreach(j, c; row.enumerate)
    {
      if(i == bot.x && j == bot.y)
        write("B");
      else
        write(texture(c));
    }
    writeln();
  }
}

struct Bot
{
  int x = 25;
  int y = 25;
  Direction last = Direction.North;

  void roam(Direction d){
    last = d;
    final switch(d)
    {
      case(Direction.North): y++; break;
      case(Direction.South): y--; break;
      case(Direction.West): x--; break;
      case(Direction.East): x++; break;
    }
  }

  void rotate(){
    final switch(last)
    {
      case(Direction.North): last = Direction.East; break;
      case(Direction.South): last = Direction.West; break;
      case(Direction.West): last = Direction.North; break;
      case(Direction.East): last = Direction.South; break;
    }
  }
}


void main()
{
  immutable BigInt[] code = readText("input01.txt").strip.split(",").map!(a => to!BigInt(a)).array.assumeUnique;

  auto tid = spawnLinked(function(immutable BigInt[] input){Program(input, ownerTid).compute;
      }, code);

//TODO dynamic card
//TODO maze solving
//I NEED A GRAPH AND DIAJKSTRA
  auto scout = new Karte[][](65,65);

  Bot bot;
  try {
    while (true) {
      int player = choice([1,2,3,4]);
      bot.last = player.to!Direction;
      send(tid, bot.last.to!BigInt);

      Status st;
      receive((BigInt i) {st = i.to!int.to!Status;});
      if(st == Status.Move)
      {
        scout[bot.x][bot.y] = Karte.Nothing;
        bot.roam(bot.last.to!Direction);
      }
      else if(st == Status.Wall)
      {
        if(bot.last == Direction.North)
          scout[bot.x][bot.y+1] = Karte.Wall;
        else if(bot.last == Direction.South)
          scout[bot.x][bot.y-1] = Karte.Wall;
        else if(bot.last == Direction.West)
          scout[bot.x-1][bot.y] = Karte.Wall;
        else if(bot.last == Direction.East)
          scout[bot.x+1][bot.y] = Karte.Wall;
        bot.rotate;
      }
      else if(st == Status.Ox)
      {
        if(bot.last == Direction.North)
          scout[bot.x][bot.y+1] = Karte.Ox;
        else if(bot.last == Direction.South)
          scout[bot.x][bot.y-1] = Karte.Ox;
        else if(bot.last == Direction.West)
          scout[bot.x-1][bot.y] = Karte.Ox;
        else if(bot.last == Direction.East)
          scout[bot.x+1][bot.y] = Karte.Ox;
        show(scout, bot);
        break;
      }
    }
  } catch (LinkTerminated e) { }

  //from
  int x = 25;
  int y = 25;

}

