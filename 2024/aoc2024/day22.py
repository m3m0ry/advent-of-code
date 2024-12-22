from boiler import AbstractDay

from collections import defaultdict

def mix(a: int, b: int):
    return a ^ b

def prune(n):
    return n % 16777216


def next_secret(secret: int):
    res = secret * 64
    res = mix(secret, res)
    res = prune(res)

    res2 = res // 32
    res2 = mix(res, res2)
    res2 = prune(res2)

    res3 = res2 * 2048
    res3 = mix(res2, res3)
    res3 = prune(res3)

    return res3


class Day22(AbstractDay):
    def preprocess(self):
        self.secrets = [int(l) for l in self.puzzle]

    def part1(self):
        secrets = self.secrets

        res = 0
        for secret in secrets:
            n = secret
            for _ in range(2000):
                n = next_secret(n)
            res += n
        return res

    def part2(self):
        secrets = self.secrets

        res = defaultdict(lambda: 0)
        for secret in secrets:
            occured = set()
            n1 = 0
            n2 = secret
            n3 = next_secret(n2)
            n4 = next_secret(n3)
            n5 = next_secret(n4)
            for _ in range(2000-3):
                n5, n4, n3, n2, n1 = next_secret(n5), n5, n4, n3, n2
                d5, d4, d3, d2, d1 = n5 % 10, n4 % 10, n3 % 10, n2 % 10, n1 % 10
                diff1 = d2 - d1
                diff2 = d3 - d2
                diff3 = d4 - d3
                diff4 = d5 - d4
                diff = (diff4, diff3, diff2, diff1)
                if diff not in occured:
                    occured.add(diff)
                    res[diff] += d5

        return max(res.values())

