import std.stdio;
import std.typecons;
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

ulong[] shoot(string[][] field, int i, int j, int steps)
{
  Tuple!(real, ulong, ulong)[][real] angles;
  foreach(k; 0..field.length.to!int)
  {
    foreach(l; 0..field[k].length.to!int)
    {
      if(!(i == k && j == l) && field[k][l] == "#")
      {
        real x = (i-k).to!real;
        real y = (j-l).to!real;
        real angle = atan2(y,x);
        angles[angle] ~= Tuple!(real, ulong, ulong)(sqrt(x^^2 + y^^2),k,l);
      }
    }
  }
  foreach(k, v; angles)
  {
    angles[k] = v.sort!"a[0] < b[0]".array;
  }
  //TODO sort the keys???
  //go from 0 to negative, then postive to 0 (without 0)
  int shots = 1;
  while(shots <= steps)
  {
    foreach(k; chain(angles.keys.sort!"a>b".filter!"a<=0", angles.keys.sort!"a>b".filter!"a>0"))
    {
      writeln(k, ": ", angles[k]);
      writeln(shots);
      if(angles[k].length != 0)
      {
        if(shots == steps)
        {
          auto last = angles[k].front;
          return [last[1], last[2]];
        }
        angles[k] = angles[k].dropOne.array;
        shots++;
      }
    }
  }

  return [1,2,4];
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

  ulong station = result.map!(a => a.maxElement).maxElement;
  ulong stationX;
  ulong stationY;
  foreach(i; 0..result.length)
  {
    foreach(j; 0..result[i].length)
    {
      if(result[i][j] == station)
      {
        stationX = i;
        stationY = j;
      }
    }
  }
  writeln(stationX, " ", stationY);
  auto last = shoot(code, stationX.to!int, stationY.to!int, 200);
  writeln(last);
}
