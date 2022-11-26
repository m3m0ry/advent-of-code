import std.stdio;
import std.math;
import std.algorithm;
import std.typecons;
import std.range;
import std.string;
import std.conv;


alias Point = Vector!int;
alias Points = bool[Point];


alias VectorReal = Vector!real;
struct Vector(T) {
    private T x, y;

    this(T x, T y) {
        this.x = x;
        this.y = y;
    }

    T distance(Point o = Point(0,0))
    {
      return abs(x - o.x) + abs(y - o.y);
    }

    auto opBinary(string op : "+")(Vector rhs) const {
        return Vector(x + rhs.x, y + rhs.y);
    }

    auto opBinary(string op : "-")(Vector rhs) const {
        return Vector(x - rhs.x, y - rhs.y);
    }

    void toString(scope void delegate(const(char)[]) sink) const {
        import std.format;
        sink.formattedWrite!"(%s, %s)"(x, y);
    }
}


Point[] parse(string[] wires)
{
  Point[] parsedWires;
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

Point[] generateLine(Point x, Point y)
{
  Point[] p;
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

Points sparseGrid(Point[] wires)
{
  Points s;
  auto current = Point(0,0);
  foreach(wire; wires)
  {
    auto next = current + wire;
    foreach(p; generateLine(current, next))
    {
      s[p] = true;
    }
    current = next;
  }
  return s;
}

Points intersect(Points a, Points b)
{
  Points c;
  foreach(key; a.keys)
    if (key in b)
      c[key] = true;
  return c;
}


int wireLength(Point a, Point[] wires)
{
  int steps;
  auto current = Point(0,0);
  foreach(wire; wires)
  {
    auto next = current + wire;
    foreach(p; generateLine(current, next))
    {
      if (p == a)
        return steps;
      steps++;
    }
    current = next;
  }
  throw new Exception("No intersection");
}

void main()
{
  auto f = File("input02.txt");

  auto lines = f.byLine;
  auto wires1 = lines.front.to!string.split(",").parse;
  lines.popFront;
  auto wires2 = lines.front.to!string.split(",").parse;

  auto grid1 = sparseGrid(wires1);
  auto grid2 = sparseGrid(wires2);

  auto intersects = intersect(grid1, grid2);
  intersects.remove(Point(0,0));


  auto c = minElement!(a=>a.wireLength(wires1)+ a.wireLength(wires2))(intersects.keys);
  writeln(c);
  writeln(c.wireLength(wires1) + c.wireLength(wires2));
}
