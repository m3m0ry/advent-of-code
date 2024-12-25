from boiler import AbstractDay

from itertools import groupby

import numpy as np

class Day25(AbstractDay):
    def preprocess(self):
        locks = []
        keys = []

        for _, g in groupby(self.puzzle, key=lambda x: not x):
            arr = np.array([[c for c in line] for line in g])
            if len(arr.flatten()) > 0:
                if arr[0,0] == '#':
                    locks.append(arr)
                else:
                    keys.append(arr)

        self.locks = locks
        self.keys = keys

    def part1(self):
        locks = self.locks
        keys = self.keys

        locks_hist = set()
        for lock in locks:
            locks_hist.add(tuple(((lock == '#').sum(axis=0) -1).tolist()))

        keys_hist = set()
        for key in keys:
            keys_hist.add(tuple(((key == '#').sum(axis=0) -1).tolist()))

        length = locks[0].shape[0]

        res = 0
        for key in keys_hist:
            # lock_search = (length - key[0], length - key[1], length - key[2], length - key[3], length - key[4])
            for lock in locks_hist:
                if all((k+l < 6 for k, l in zip(key, lock))):
                    res += 1

        return res

    def part2(self):
        return None

