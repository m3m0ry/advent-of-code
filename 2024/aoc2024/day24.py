from boiler import AbstractDay

from collections import defaultdict

import re
import queue


def compute(op, registers):
    match op[0]:
        case 'AND':
            registers[op[1]] = registers[op[2]] and registers[op[3]]
        case 'OR':
            registers[op[1]] = registers[op[2]] or registers[op[3]]
        case 'XOR':
            registers[op[1]] = registers[op[2]] ^ registers[op[3]]
        case _:
            raise NotImplementedError('No such op!')

class Day24(AbstractDay):
    def preprocess(self):
        x = 0
        for i, l in enumerate(self.puzzle):
            if not l:
                x = i
                break
        
        registers = {}
        for l in self.puzzle[:x]:
            reg, num = l.split(': ')
            registers[reg] = bool(int(num))
        
        pattern = re.compile(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)')
        ops = []
        for l in self.puzzle[x+1:]:
            m = pattern.match(l)
            ops.append((m[2], m[4], m[1], m[3]))

        self.registers = registers
        self.ops = ops

    def part1(self):
        regs = self.registers
        ops = self.ops
        ops_queue = queue.SimpleQueue()
        for op in ops:
            ops_queue.put(op)

        while not ops_queue.empty():
            op = ops_queue.get()
            if op[2] in regs and op[3] in regs:
                compute(op, regs)
            else:
                ops_queue.put(op)

        zs = [reg for reg in regs if 'z' == reg[0]]
        zs.sort()
        num = ''.join(str(int(regs[i])) for i in reversed(zs))

        return int(num, 2)

    def part2(self):
        node = 0
        ops = self.ops




        graph = defaultdict(lambda: list())
        node = 0
        for op in ops:
            graph[op[2]].append(f'{op[0]}{node}')
            graph[op[3]].append(f'{op[0]}{node}')
            graph[f'{op[0]}{node}'].append(op[1])
            node += 1

        # Necesary swaps so my check of full adders works:
        graph['XOR64'] = ['z10']
        graph['AND78'] = ['mkk']

        graph['OR196'] = ['qbw']
        graph['XOR140'] = ['z14']

        graph['AND156'] = ['wjb']
        graph['XOR20'] = ['cvp']

        graph['AND45'] = ['wcb']
        graph['XOR111'] = ['z34']

        # Graph visualization for debugging
        with open('graph', 'w') as f:
            f.write('digraph D {\n')
            for op in ops:
                f.write(f'{op[2]} -> {op[0]}{node}\n')
                f.write(f'{op[3]} -> {op[0]}{node}\n')
                f.write(f'{op[0]}{node} -> {op[1]}\n')
                node += 1
            f.write('}\n')
        
        c = None

        ops = graph['x00']
        assert ops == graph['y00']
        assert len(ops) == 2
        one, two = ops
        if one[:3] == 'XOR':
            out = graph[one]
            c = graph[two]
        elif one[:3] == 'AND':
            out = graph[two]
            c = graph[one]

        assert len(out) == 1
        assert 'z00' == out[0]

        
        assert len(c) == 1
        c = c[0]
        
        for i in (f'{i}{j}' for i in range(5) for j in range(10)):
            if i == '00':
                continue
            if i == '45':
                break

            ops = graph['x' + i]
            assert ops == graph['y' + i]
            assert len(ops) == 2
            one, two = ops

            if one[:3] == 'XOR':
                xor_out = graph[one]
                and_out = graph[two]
            elif one[:3] == 'AND':
                and_out = graph[one]
                xor_out = graph[two]
            assert len(xor_out) == 1
            xor_out = xor_out[0]
            assert len(and_out) == 1
            and_out = and_out[0]

            cs = graph[c]
            xors = graph[xor_out]
            assert len(cs) == 2
            assert len(xors) == 2, xors

            if cs[0][:3] == 'XOR':
                xor_c = cs[0]
                and_c = cs[1]
                assert and_c[:3] == 'AND'
            elif cs[1][:3] == 'XOR':
                xor_c = cs[1]
                and_c = cs[0]
                assert and_c[:3] == 'AND'

            if xors[0][:3] == 'XOR':
                xor_x = xors[0]
                and_x = xors[1]
                assert and_x[:3] == 'AND'
            elif xors[1][:3] == 'XOR':
                xor_x = xors[1]
                and_x = xors[0]
                assert and_x[:3] == 'AND'
            
            assert xor_x == xor_c
            assert and_x == and_c
            
            # zXX = c XOR xor_out
            z = graph[xor_c]
            assert len(z) == 1, z
            z = z[0]
            assert 'z'+i == z, f'{'z'+i} {z}'

            # (c AND xor_out) OR and_out == next_c
            second_and = graph[and_x]
            assert len(second_and) == 1
            second_and = second_and[0]

            one_or = graph[second_and]
            assert len(one_or) == 1, f'{one_or} from {second_and}'
            one_or = one_or[0]
            same_or = graph[and_out]
            assert len(same_or) == 1
            same_or = same_or[0]
            assert same_or == one_or

            next_c = graph[one_or]
            assert len(next_c) == 1
            c = next_c[0]

        # See above how graph was fixed
        swaps = ['z10', 'mkk', 'qbw', 'z14', 'wjb', 'cvp', 'wcb', 'z34']
        return ','.join(sorted(swaps))

