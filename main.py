import data, mistakes
from levenshtein import levenshtein, lightweight_lvs

import random, string
from itertools import permutations


def song_comparison(s, t):
    s, t = s.split(), t.split()
    similarity = 10 ** 9
    if len(s) > len(t):
        return levenshtein(' '.join(s), ' '.join(t))

    for p in permutations(t, len(s)):
        #print(s, p)
        similarity = min(similarity, sum(levenshtein(u, v) for (u, v) in zip(s, p)))

    return similarity


def noise(s, Q = 3):
    for i in range(Q):
        j = random.choice(range(len(s)))
        c = random.choice(string.ascii_lowercase)
        s = s[:j] + c + s[j + 1:]
    return s


def search(s, Q = 2): #old
    ans = list(sorted(data.songs, key = lambda x : song_comparison(s, x)))

    return list(filter(lambda x : song_comparison(s, x) <= Q, ans))


def top_frequent(s, Q):
    #return [s] if s in data.inv else []
    return [key for key in data.inv if abs(len(s) - len(key)) <= Q and lightweight_lvs(s, key) <= Q + 1]


def full_search(s, Q = 2):
    s = ' '.join(t.lower() for t in s.split())

    words = s.split()
    #print(words)
    #candidates = [data.inv[x] for x in top_frequent(word) for word in words]

    candidates = []
    for word in words:
        array = []
        for x in top_frequent(word, Q):
            #print(x)
            #print(word)
            #print(x)

            array.extend(data.inv[x])
        candidates += [array]

    assert candidates
    #print(len(candidates))
    #print(candidates)

    intersection = set(data.songs)

    for can in candidates:
        if len(can) > 5:
            intersection &= set(can)

    return [x for x in intersection if song_comparison(s, x) <= Q]


s = input()
res = full_search(s, 1)
print('\n'.join(sorted(res)))
print()
res = full_search(s, 2)
print('\n'.join(sorted(res)))
print()