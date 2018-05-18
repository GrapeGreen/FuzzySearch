from collections import defaultdict
from levenshtein import Operation
import re

d = defaultdict(float)

c = defaultdict(float)

types = defaultdict(lambda : defaultdict(tuple))

total = 0

with open('mistakes.txt', 'r') as f:
    for line in f:
        line = line.split()
        freq = int(line[-1])
        line[0] = ''.join(str(x) for x in line[:-1])
        old, new = re.split('[|]', line[0])

        d[(old, new)] += freq
        total += freq

        TYPE = Operation.NONE

        if len(old) > len(new):
            TYPE = Operation.DELETE if old[0] != old[-1] or len(old) == 1 else Operation.SINGLE
        elif len(old) < len(new):
            TYPE = Operation.ADD if new[0] != new[-1] or len(new) == 1 else Operation.DOUBLE
        else:
            if len(old) > 1 and old[0] == new[-1] and old[-1] == new[0]:
                TYPE = Operation.TRANSPOSE
            else:
                TYPE = Operation.SUBSTITUTE

        types[TYPE][(old, new)] = freq

        for len_x in range(1, 3):
            for len_y in range(1, 3):
                for i in range(len(old) - len_x + 1):
                    for j in range(len(new) - len_y + 1):
                        c[(old[i : i + len_x], new[j : j + len_y])] += freq


for key in d:
    d[key] /= total
