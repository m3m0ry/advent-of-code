import std.stdio;
import std.file : readText;
import std.conv;
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
  program = compute(program);

  writeln(program[0]);
}
