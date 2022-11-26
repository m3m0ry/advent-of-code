import std.stdio;
import std.conv;


int fuel(int mass)
{
  return mass/3 -2;
}


void main()
{
  auto f = File("input01.txt");
  int output = 0;
  foreach(line; f.byLine)
  {
    output += fuel(to!int(line));
  }

  writeln(output);
}
