import std.stdio;
import std.math;
import std.algorithm;
import std.typecons;
import std.range;
import std.string;
import std.conv;


alias Point = Vector!int;
alias Points = Point[];

struct Vector(T) {
    private T x, y;

    T distance(const Point o = Point(0,0)) const
    {
      return abs(x - o.x) + abs(y - o.y);
    }

    int opCmp(ref const Vector!T s) const {
      if (x < s.x)
        return -1;
      else if (x > s.x)
        return 1;
      else
      {
        if (y < s.y)
          return -1;
        else if (y > s.y)
          return 1;
        else
          return 0;
      }
    }

    auto opBinary(string op)(Vector rhs) const {
        return mixin(`Vector(x`~ op ~`rhs.x, y`~ op ~`rhs.y)`);
    }

    void toString(scope void delegate(const(char)[]) sink) const {
        import std.format;
        sink.formattedWrite!"(%s, %s)"(x, y);
    }
}


Points parse(string[] wires)
{
  Points parsedWires;
  parsedWires.length = wires.length;
  foreach(i, wire; wires)
  {
    switch(wire[0])
    {
      default: throw new Exception(format!"WTF: %s"(wire));
      case 'R': parsedWires[i] = Point(to!int(wire[1 .. $]), 0); break;
      case 'L': parsedWires[i] = Point(-to!int(wire[1 .. $]), 0); break;
      case 'U': parsedWires[i] = Point(0, to!int(wire[1 .. $])); break;
      case 'D': parsedWires[i] = Point(0, -to!int(wire[1 .. $])); break;
    }
  }
  return parsedWires;
}

Points generateLine(Point x, Point y)
{
  Points p;
  if(x.y == y.y)
  {
    foreach(i; min(x.x, y.x) .. max(x.x, y.x))
    {
        p ~= Point(i,x.y);
    }
  }
  else if (x.x == y.x)
  {
    foreach(i; min(x.y, y.y) .. max(x.y, y.y))
    {
        p ~= Point(x.x,i);
    }
  }
  else
    throw new Exception("Fuck");
  return p;
}

Points sparseGrid(Points wires)
{
  Points s;
  auto current = Point(0,0);
  foreach(wire; wires)
  {
    auto next = current + wire;
    foreach(p; generateLine(current, next))
    {
      s ~= p;
    }
    current = next;
  }
  return s;
}

void main()
{
  auto f = File("input02.txt");

  auto lines = f.byLine;
  auto wires1 = lines.front.to!string.split(",").parse;
  lines.popFront;
  auto wires2 = lines.front.to!string.split(",").parse;

  auto grid1 = sparseGrid(wires1).sort;
  auto grid2 = sparseGrid(wires2).sort;

  writeln(grid1);
  writeln(grid2);
  auto intersects = setIntersection(grid1, grid2);
  intersects.popFront;
  writeln(intersects);

  auto c = minElement!(a=>a.distance)(intersects);
  writeln(c);
  writeln(c.distance);
}
