import std.stdio;
import std.conv;
import std.format;
import std.algorithm;
import std.array;
import std.math : abs, sgn;
import std.format;

struct Moon
{
  int[3] pos;
  int[3] vel;

  int potential()
  {
    return pos.fold!((a, b) => abs(a) + abs(b));
  }

  int kinetic()
  {
    return vel.fold!((a, b) => abs(a) + abs(b));
  }

  int total()
  {
    return potential * kinetic;
  }

  void applyVelocity()
  {
    pos[] += vel[];
  }

  void gravity(Moon o)
  {
    foreach (i; 0 .. pos.length)
    {
      vel[i] -= o.pos[i] < pos[i];
      vel[i] += o.pos[i] > pos[i];
    }
 }

  string toString()
  {
    return format!"pos=<x=%d, y=%d, z=%d>, vel=<x=%d, y=%d, z=%d>"(pos[0],
        pos[1], pos[2], vel[0], vel[1], vel[2]);
  }
}

void main()
{
  auto f = File("input01.txt");
  Moon[] moons;
  foreach (line; f.byLine)
  {
    int x, y, z;
    line.formattedRead!"<x=%d, y=%d, z=%d"(x, y, z);
    moons ~= Moon([x, y, z]);
  }

  foreach (i; 0 .. 1_000)
  {
    foreach (ref moon; moons)
    {
      foreach (o; moons)
      {
        moon.gravity(o);
      }
    }
    foreach (ref moon; moons)
    {
      moon.applyVelocity;
    }
  }
  writeln("Total system energy: ", moons.map!(a => a.total).sum);
}
