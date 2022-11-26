import std.stdio;
import std.conv;
import std.string;
import std.algorithm;
import std.array;
import std.range;


bool twoAdjacent(int number)
{
  auto ns = number.to!string.split("").map!(to!int);
  auto last = ns.front;
  foreach(n; ns.dropOne)
  {
    if (last == n)
      return true;
    last = n;
  }
  return false;
}

bool hasTwo(int number)
{
  auto ns = number.to!string.split("").map!(to!int);
  foreach(n; ns)
    if(ns.count(n) == 2)
      return true;
  return false;
}


bool higher(int number)
{
  auto ns = number.to!string.split("").map!(to!int);
  auto last = ns.front;
  foreach(n; ns.dropOne)
  {
    if (last > n)
      return false;
    last = n;
  }
  return true;
}

void main()
{
  int low = 165432;
  int high = 707912;
  int count = 0;
  foreach(i; low .. high)
  {
    if(twoAdjacent(i) && higher(i) && hasTwo(i))
      count++;
  }
  writeln(count);
}
