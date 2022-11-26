import std.stdio;
import std.conv;


int fuel(int mass)
{
  auto f = mass/3 -2;
  if (f <= 0)
    return 0;
  else
  {
    return fuel(f) + f;
  }
}

void main()
{
  auto f = File("input02.txt");
  int output = 0;
  foreach(line; f.byLine)
  {
    output += fuel(to!int(line));
  }

  writeln(output);
}
