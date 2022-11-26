import std.stdio;
import std.file : readText;
import std.conv;
import std.array;
import std.format;
import std.range;
import std.algorithm;
import std.string;

int[] set(int[] program, int n, int value)
{
  program[program[n]] = value;
  return program;
}

int get(int[] program, int n)
{
  return program[program[n]];
}

int[] operation(string op)(int[] program, int instructionPointer)
{
    auto p = program[];
    return set(p, instructionPointer+3, mixin(`get(p, instructionPointer+2)` ~ op ~ `get(p,instructionPointer+1)`));
}

int[] compute(int[] program, int instructionPointer = 0)
{
  int instruction = program[instructionPointer];
  if (instruction == 1)
  {
    return compute(operation!"+"(program, instructionPointer), instructionPointer+4);
  }
  else if (instruction == 2)
  {
    return compute(operation!"*"(program, instructionPointer), instructionPointer+4);
  }
  else if (instruction == 99)
  {
    return program;
  }
  else
  {
    throw new Exception("Invalid instruction");
  }
}


void main()
{
  int[] program = readText("input01.txt").strip.split(",").map!(a => to!int(a)).array;
  foreach(i; 0 .. 99)
  {
    foreach(j; 0 .. 99)
    {
      auto p = program.array;
      p[1] = i;
      p[2] = j;
      p = compute(p);
      if (19690720 == p[0])
      {
        writeln(format!"%02d"(p[1]), format!"%02d"(p[2]));
        return;
      }
    }
  }
}
