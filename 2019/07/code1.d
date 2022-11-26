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

struct Program
{
  int ip = 0;
  int[] program;

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
  return p;
}

Program compute(Program program)
{
  int instruction = program.op.format!"%05d"[$-2 .. $].to!int;
  program = ops[instruction](program);

  if (instruction == 99)
  {
    return program;
  }
  else
  {
    return compute(program);
  }
}

void main()
{
  int[] code = readText("input01.txt").strip.split(",").map!(a => to!int(a)).array;
  //code = "3,9,7,9,10,9,4,9,99,-1,8".strip.split(",").map!(a=>to!int(a)).array;
  auto program = Program(0, code);
  int best;
  foreach(permutation; iota(5).permutations)
  {
    auto output = 0;
    foreach(p; permutation)
    {
      auto temp = program;
      ioStack.insertBack(p);
      ioStack.insertBack(output);
      compute(temp);
      output = ioStack.front;
      ioStack.removeFront;
      stderr.writeln(output);
      stderr.writeln(ioStack.empty);
    }
    best = max(best, output);
  }
  writeln(best);
}
