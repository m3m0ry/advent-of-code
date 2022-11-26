module code2;
import std.stdio;
import std.conv;
import std.regex;
import std.typecons;
import std.string;
import std.format;
import std.algorithm;
import std.exception;
import std.array;
import std.math;
import std.bigint;

alias Chemical = Tuple!(string, BigInt);
Chemical chemical(T)(T react)
{
  string s;
  int i;
  react.formattedRead!"%d %s"(i, s);
  return Chemical(s,i.BigInt);
}

struct Reaction
{
  Chemical output;
  Chemical[] input;
}

Reaction findReaction(string target, Reaction[] reactions)
{
  foreach(reaction; reactions)
  {
    if (reaction.output[0] == target)
    {
      return reaction;
    }
  }
  throw new Exception("No such reaction");
}

Chemical build(Chemical target, Chemical source, Reaction[] reactions)
{
  Chemical[] want = [target];
  Chemical[] newWant;
  BigInt[string] rest;
  while(!want.all!(a => a[0] == "ORE"))
  {
    foreach(w; want)
    {
      if(w[0] == source[0])
      {
        newWant ~= w;
      }
      else
      {
        Reaction targetRule = findReaction(w[0], reactions);
        //get rest if any
        BigInt todo;
        if(w[0] in rest && rest[w[0]] > 0)
        {
          todo = w[1] - rest[w[0]];
          if(todo < 0)
          {
            todo = 0;
            rest[w[0]] -= w[1];
          }
          else
          {
            rest[w[0]] = 0;
          }
        }
        else if(w[1] > 0)
          todo = w[1];
        //BigInt reacts = ceil(todo.to!real / targetRule.output[1].to!real).to!int.to!BigInt;
        //BigInt remainder = targetRule.output[1] * reacts - todo;
        BigInt q;
        BigInt r;
        divMod(todo, targetRule.output[1], q, r);
        BigInt reacts = q;
        BigInt remainder;
        if (r != 0)
        {
          reacts = q +1;
          remainder = targetRule.output[1] - r;
        }

        if(w[0] in rest)
          rest[w[0]] += remainder;
        else if(remainder != 0)
          rest[w[0]] = remainder;
        foreach(chem; targetRule.input)
        {
          chem[1] *= reacts;
          newWant ~= chem; 
        }
      }
    }
    want = newWant;
    newWant.length = 0;
  }
  return want.fold!((a,b) => Chemical("ORE", a[1] + b[1]))(Chemical("ORE", 0.BigInt));
}

void main()
{
  auto f = File("input01.txt");
  Reaction[] reactions;
  foreach(line; f.byLine)
  {
    reactions ~= Reaction(line.to!string.split(" => ")[1].chemical,
                          line.to!string.split(" => ")[0].split(", ").map!( a => chemical(a)).array);
  }
  //reactions.each!(a => a.writeln);
  auto need = build(Chemical("FUEL", 1.BigInt), Chemical("ORE", 0.BigInt), reactions);
  writeln("Task1: ", need);

  BigInt ore = need[1];
  BigInt maxOre = BigInt(1_000_000)*BigInt(1_000_000);
  BigInt step = maxOre;
  for(BigInt fuel = maxOre/ore;;fuel += step)
  {
    need = build(Chemical("FUEL", fuel), Chemical("ORE", 0.BigInt), reactions);
    ore = need[1];
    if(ore > maxOre)
    {
      if(step == 1)
      {
        writeln("Fuel: ", fuel-1);
        break;
      }
      fuel -= step;
      step /= 10;
    }
  }
}
