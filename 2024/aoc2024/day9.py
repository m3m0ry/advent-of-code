from boiler import AbstractDay

from itertools import groupby

def next_empty(empty, disk):
    while disk[empty] != -1 and empty < len(disk):
        empty += 1
    return empty

def b4_last(last, disk):
    while disk[last] == -1 and last >= 0:
        last -= 1
    return last

def first_large_enough(size, disk):
    for i, e in enumerate(disk):
        if e[0] == -1 and e[1] >= size:
            return i
    return None

def last_entry(entry, disk):
    for i, e in enumerate(reversed(disk)):
        if e[0] == entry:
            return len(disk) - i - 1
    return None

class Day9(AbstractDay):
    def preprocess(self):
        assert len(self.puzzle) == 1, 'Check input'
        self.puzzle = [int(p) for p in self.puzzle[0]]

    def part1(self):
        puzzle = self.puzzle
        disk = []
        space = False
        id_num = 0
        for p in puzzle:
            if space:
                disk.extend(p* [-1])
            else:
                disk.extend(p* [id_num])
                id_num += 1
            space = not space

        empty = next_empty(0, disk)
        last = b4_last(len(disk)-1, disk)
        while empty < last:
            disk[last], disk[empty] = disk[empty], disk[last]
            empty = next_empty(empty, disk)
            last = b4_last(last, disk) 

        res = 0
        for i, id_num in enumerate(disk):
            if id_num == -1:
                break
            res += i * id_num
        return res

    def part2(self):
        puzzle = self.puzzle
        disk = []
        space = False
        id_num = 0
        for p in puzzle:
            if space:
                if p > 0:
                    disk.append((-1, p))
            else:
                disk.append((id_num, p))
                id_num += 1
            space = not space

        entries = [d[0] for d in reversed(disk) if d[0] != -1]
        for file in entries:
            entry = last_entry(file, disk)
            space = first_large_enough(disk[entry][1], disk)
            if not space:
                continue
            if space > entry:
                continue
            c = disk[entry][1]
            left = disk[space][1] - c
            disk[space] = disk[entry]
            disk[entry] = (-1, c)
            if left > 0:
                disk.insert(space+1, (-1, left))
        
        res = 0
        i = 0
        for entry in disk:
            if entry[0] != -1:
                for j in range(entry[1]):
                    res += i * entry[0]
                    i += 1
            else:
                i += entry[1]
        return res

