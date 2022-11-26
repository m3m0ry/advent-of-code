module code2;

import std.stdio;
import std.file : readText;
import std.conv;
import std.range;
import std.algorithm;
import std.string;
import std.math;


int[][] assemble(size_t length, int[] basePattern = [0,1,0,-1])
{
  int[][] m = new int[][](length, length);
  foreach(i; 0..length)
  {
    m[i][] = pattern(i, length, basePattern)[];
  }
  return m;
}

int[] pattern(ulong element, const size_t length = 8, int[] basePattern = [0,1,0,-1])
{
  int[] result;
  int[] pattern;
  foreach(p; basePattern)
  {
    foreach(i; 0..element+1)
    {
      pattern ~= p;
    }
  }
  loop: foreach(i, v; pattern.cycle.enumerate)
  {
    if(i == 0)
      continue;
    else if(i == length + 1)
      break loop;
    result ~= v;
  }
  return result;
}

int[] fft(int[] signal, int[][] matrix){
  int[] result = new int[](signal.length);
  int[] temp = new int[](signal.length);
  foreach(i, row; matrix.enumerate)
  {
    temp[] = row[] * signal[];
    result[i] = temp.sum.abs;
    result[i] %= 10;
  }
  return result;
}


void main()
{
  int[] signal = readText("input01.txt").strip.split("").map!(a => to!int(a)).array;
  writeln(signal.length);
  int offset = signal[0..7].map!(a => a.to!string).join("").to!int;
  writeln(offset);
  signal = signal.repeat(10_000).joiner.drop(offset).array;
  writeln(signal.length);
  foreach(i; 0..100){
    writeln("Phase: ", i);
    int cumulativeSum = 0;
    foreach(j; iota(signal.length.to!int -1, -1, -1))
    {
      cumulativeSum += signal[j];
      signal[j] = cumulativeSum % 10;
    }
  }
  writeln(signal[0..8]);
}
