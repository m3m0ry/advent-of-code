import std.stdio;
import std.conv;
import std.math;
import std.range;
import std.string;
import std.algorithm;
import std.string;
import std.file;
import std.array;

ulong asteroids(string[][] field, int i, int j)
{
  real[real] angles;
  foreach(k; 0..field.length.to!int)
  {
    foreach(l; 0..field[k].length.to!int)
    {
      if(!(i == k && j == l) && field[k][l] == "#")
      {
        real x = (i-k).to!real;
        real y = (j-l).to!real;
        real angle = atan2(y,x);
        real distance = sqrt(x^^2 + y^^2);
        angles[angle] = min(distance, angles.get(angle, real.max));
      }
    }
  }
  return angles.length;
}


void main()
{
  string[][] code = File("input01.txt").byLine.map!(a => a.to!string.strip.split("")).array;
  ulong[][] result = code.map!(a => a.map!(b => ulong.init).array).array;
  foreach(i; 0..code.length)
  {
    foreach(j; 0..code[i].length)
    {
      if(code[i][j] == "#")
        result[i][j] = asteroids(code, i.to!int, j.to!int);
    }
  }
  writeln(result.map!(a => a.maxElement).maxElement);
}
