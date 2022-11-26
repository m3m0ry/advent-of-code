import std.stdio;
import std.conv;
import std.string;
import std.algorithm;

ulong distance(string[string] orbits, string from, string to)
{
  int result;
  while(from in orbits)
  {
    from = orbits[from];
    if (from == to)
      return result;
    result++;
  }
  throw new Exception(format!"No route from %s to %s"(from, to));
}

ulong min(string[string] orbits, string from, string to)
{
  string[] candidatesTo;
  string[] candidatesFrom;
  for(auto c=from; c in orbits; c=orbits[c])
    candidatesTo ~= c;
  for(auto c=to; c in orbits; c=orbits[c])
    candidatesFrom ~= c;
  foreach(c; candidatesFrom)
    if(candidatesTo.canFind(c))
      return distance(orbits, from, c) + distance(orbits, to, c);
  throw new Exception(format!"No route from %s to %s"(from, to));
}


void main()
{
  auto f = File("input01.txt");
  string[string] orbits;
  foreach(line; f.byLine)
  {
    auto o = line.to!string.split(")");
    orbits[o[1]] = o[0];
  }

  writeln(min(orbits, "YOU", "SAN"));
}
