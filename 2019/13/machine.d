import std.stdio;
import std.file : readText;
import std.conv;
import std.range;
import std.algorithm;
import std.string;
import std.exception;
import std.container;
import std.bigint;
import std.traits;
import std.concurrency;

Program function(Program)[int] ops;

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
  ops[9] = &adjustBase;
  ops[99] = &opStop;
}

enum Status{ Normal, Stop, Interrupt }
enum Mode {
  Position = 0,
  Immediate = 1,
  Relative = 2,
}

struct Program
{
  BigInt ip;
  BigInt[BigInt] program;
  Status state = Status.Normal;
  BigInt relativeBase;
  Tid output;

  this(BigInt[BigInt] p)
  {
    program = p;
  }

  this(immutable BigInt[] p, Tid o)
  {
    output = o;
    this(p);
  }

  this(immutable BigInt[] p)
  {
    foreach(i, l; enumerate(p))
      program[BigInt(i)] = BigInt(l);
  }

  BigInt op()
  {
    return program[ip];
  }

  ref BigInt get(BigInt i)
  {
    if (i !in program)
      program[i] = BigInt.init;
    return program[i];
  }
  
  ref BigInt opIndex(BigInt i, int mode = Mode.Position)
  {
    final switch (mode){
      case Mode.Position:
        return get(get(i));
      case Mode.Immediate: 
        return get(i);
      case Mode.Relative:
        return get(relativeBase + get(i));
    }
  }
  void print()
  {
    writeln("IP: ", ip);
    writeln("RP: ", relativeBase);
    foreach(key; program.keys.sort)
    {
      write(key, ": ", program[key]);
      write(",");
    }
    writeln();
  }

  @property size_t opDollar(size_t dim : 0)() { return program.length;}
}

int mode(BigInt op, int i)
{
  return op.format!"%05d"[i..i+1].to!int;
}

Program adjustBase(Program p)
{
  p.relativeBase += p[p.ip+1, mode(p.op, 2)];
  p.ip += 2;
  return p;
}

Program opArithmetic(string op)(Program p)
{
    auto t = mixin(`p[p.ip+1, mode(p.op, 2)]` ~ op ~ `p[p.ip+2, mode(p.op, 1)]`);
    static if (isBoolean!(typeof(t)))
      p[p.ip+3, mode(p.op, 0)] = BigInt(t.to!int);
    else
      p[p.ip+3, mode(p.op, 0)] = t;
    p.ip += 4;
    return p;
}

Program opRead(Program p)
{
  send(p.output, -2.BigInt);
  send(p.output, 0.BigInt);
  send(p.output, 0.BigInt);
  p[p.ip+1, mode(p.op, 2)] = receiveOnly!BigInt;
  p.ip += 2;
  return p;
}

Program opWrite(Program p)
{
  auto t = p[p.ip+1, mode(p.op, 2)];
  send(p.output, t);
  p.ip += 2;
  return p;
}

Program opJump(string op)(Program p)
{
  if (mixin(`p[p.ip+1, mode(p.op, 2)]`~(op)~`BigInt(0)`))
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
  while(program.state == Status.Normal)
  {
    int instruction = program.op.format!"%05d"[$-2 .. $].to!int;
    program = ops[instruction](program);
  }
  return program;
}
