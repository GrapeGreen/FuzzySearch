import data, mistakes, noisy_channel
from levenshtein import levenshtein, lightweight_lvs, min_weight_max_matching
from timer import timer

import random, string
from itertools import permutations
from collections import defaultdict


def song_comparison(s, t):
    s, t = s.split(), t.split()

    similarity = levenshtein(' '.join(s), ' '.join(t))

    n, m = len(s), len(t)

    if n > m:
        return similarity

    if len(n) > 2:
        #print(s, t)
        arr = [[10 ** 9 for i in range(m)] for j in range(n)]
        #print(arr)
        for i, u in enumerate(s):
            for j, v in enumerate(t):
                #print(i, j)
                arr[i][j] = levenshtein(u, v)

        #print(arr)
        return min_weight_max_matching(n, m, arr)


    d = {(u, v) : levenshtein(u, v) for u in s for v in t}
    for p in permutations(t, n):
        #print(s, p)
        similarity = min(similarity, sum(d[(u, v)] for (u, v) in zip(s, p)))

    return similarity


@timer
def top_frequent(s, Q):
    res = noisy_channel.calculate_all(s, Q)
    return res


@timer
def full_search(s, Q = 2):
    print('Accuracy = {}'.format(Q))
    s = ' '.join(t.lower() for t in s.split())

    words = s.split()
    #print(words)

    candidates = []
    for word in words:
        array = []
        for x in top_frequent(word, Q):
            array.extend(data.inv[x])
        candidates += [array]

    assert candidates
    #print(len(candidates))
    #print(candidates)

    intersection = set(data.songs)

    for can in candidates:
        if len(can) > 5:
            intersection &= set(can)

    print('shortlist : ', intersection)
    return [x for x in intersection if song_comparison(s, x) <= Q]


s = input()
res = full_search(s, 1)
print('\n'.join(sorted(res)))
print()

res = full_search(s, 2)
print('\n'.join(sorted(res)))
print()


#res = full_search(s, 3)
#print('\n'.join(sorted(res)))
#print()