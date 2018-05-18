from collections import defaultdict
import re

d = defaultdict(float)

total = 0

with open('mistakes.txt', 'r') as f:
    for line in f:
        line = line.split()
        freq = int(line[-1])
        line[0] = ''.join(str(x) for x in line[:-1])
        #print(line)
        old, new = re.split('[|]', line[0])
        d[(old, new)] += freq
        total += freq

for key in d:
    d[key] /= total
