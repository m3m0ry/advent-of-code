import std.stdio;
import std.conv;
import std.string;

ulong indirect2(string[string] orbits, string o)
{
  ulong result;
  while (o in orbits)
  {
    o = orbits[o];
    result++;
  }
  return result;
}


ulong indirect(string[string] orbits)
{
  ulong result;
  foreach(o; orbits)
  {
    result += indirect2(orbits, o);
  }
  return result;
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

  writeln(orbits);
  writeln(orbits.length + indirect(orbits));
}
