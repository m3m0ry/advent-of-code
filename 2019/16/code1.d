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
  int[] signal = readText("input02.txt").strip.split("").map!(a => to!int(a)).array;
  int[][] matrix = assemble(signal.length);
  matrix.each!(a => writeln(a));
  foreach(i; 0..100){
    signal = fft(signal, matrix);
  }
  writeln(signal[0..8]);
}
