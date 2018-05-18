from collections import defaultdict

songs = []

d = defaultdict(int)

inv = defaultdict(list)

total = 0

with open('db.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        song = line[:-1].split()
        t = ' '.join(str(s).lower() for s in song)

        songs.append(t)
        total += len(song)

        for s in song:
            d[s.lower()] += 1
            inv[s.lower()].append(t)


for key in d:
    d[key] /= total