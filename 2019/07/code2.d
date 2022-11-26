import std.stdio;
import std.file : readText;
import std.conv;
import std.range;
import std.algorithm;
import std.string;
import std.exception;
import std.container;


Program function(Program)[int] ops;
DList!int ioStack;

static this()
{
  ops[1] = &opArithmetic!"+";
  ops[2] = &opArithmetic!"*";
  ops[3] = &opRead;
  ops[4] = &opWrite;
  ops[5] = &opJump!"!=";
  ops[6] = &opJump!"==";
  ops[7] = &opArithmetic!"<";
  ops[8] = &opArithmetic!"==";
  ops[99] = &opStop;
}

enum Status{ Normal, Stop, Interrupt }

struct Program
{
  int ip = 0;
  int[] program;
  Status state = Status.Normal;

  int op()
  {
    return program[ip];
  }

  ref int opIndex(size_t i, int mode)
  {
    if (mode == 1)
    {
      return program[i];
    }
    else if (mode == 0)
    {
      return program[program[i]];
    }
    throw new Exception("Invalid mode");
  }

  ref int opIndex(size_t i) { return program[i];}

  @property int opDollar(size_t dim : 0)() { return program.length;}
}

int mode(int op, int i)
{
  return op.format!"%05d"[i..i+1].to!int;
}

Program opArithmetic(string op)(Program p)
{
    p[p.ip+3, mode(p.op, 0)] = mixin(`p[p.ip+1, mode(p.op, 2)]` ~ op ~ `p[p.ip+2, mode(p.op, 1)]`);
    p.ip += 4;
    return p;
}

Program opRead(Program p)
{
  write("Input number:");
  if(ioStack.empty)
    p[p.ip+1, mode(p.op, 2)] = readln.strip.to!int;
  else
  {
    p[p.ip+1, mode(p.op, 2)] = ioStack.front;
    writeln(ioStack.front);
    ioStack.removeFront;
  }
  p.ip += 2;
  return p;
}

Program opWrite(Program p)
{
  auto t = p[p.ip+1, mode(p.op, 2)];
  writeln("Output: ", t);
  ioStack.insertBack(t);
  p.ip += 2;
  //Day 07 Specific
  p.state = Status.Interrupt;
  return p;
}

Program opJump(string op)(Program p)
{
  if (mixin(`p[p.ip+1, mode(p.op, 2)]`~(op)~`0`))
    p.ip = p[p.ip+2, mode(p.op, 1)];
  else
    p.ip += 3;
  return p;
}

Program opStop(Program p)
{
  p.state = Status.Stop;
  return p;
}

Program compute(Program program)
{
  auto s = program.state;
  if(s == Status.Stop)
    return program;
  else if (s == Status.Interrupt)
  {
    program.state = Status.Normal;
    return program;
  }
  int instruction = program.op.format!"%05d"[$-2 .. $].to!int;
  program = ops[instruction](program);
  return compute(program);
}

void main()
{
  int[] code = readText("input01.txt").strip.split(",").map!(a => to!int(a)).array;
  code = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".strip.split(",").map!(a=>to!int(a)).array;
  //code = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".strip.split(",").map!(a=>to!int(a)).array;
  //code = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".strip.split(",").map!(a=>to!int(a)).array;
  auto program = Program(0, code);
  int best;
  foreach(permutation; iota(5, 10).permutations)
  {
    //if(permutation.array != [9,8,7,6,5])//[9,7,8,5,6])
    //  continue;
    Program[5] programs;
    programs[0 .. $] = program;
    auto first = true;
    ioStack.clear;
    ioStack.insertFront(0);
    int runs;
    while(programs[$-1].state != Status.Stop)
    {
      foreach(i, p; permutation.enumerate)
      {
        writeln("Phase: ", i);
        foreach(e; ioStack)
          writeln("IO: ", e);
        if (first)
          ioStack.insertFront(p);
        programs[i] = compute(programs[i]);
      }
      first = false;
      programs.each!(a => writeln(a.state));
    }
    best = max(best, ioStack.front);
    if(best == ioStack.front)
      writeln(permutation);
  }
  writeln(best);
}
