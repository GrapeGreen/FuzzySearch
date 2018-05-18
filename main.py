import data, mistakes, noisy_channel
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


def top_frequent(s, Q):
    res = noisy_channel.calculate_all(s, Q)
    return res

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
        #if len(can) > 5:
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