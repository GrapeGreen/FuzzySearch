import data, mistakes
from levenshtein import levenshtein

import random, string
from itertools import permutations


def song_comparison(s, t): #full comparison for
    s, t = s.split(), t.split()
    similarity = 10 ** 9
    if len(s) > len(t):
        return levenshtein(' '.join(s), ' '.join(t))

    for p in permutations(t, len(s)):
        similarity = min(similarity, sum(levenshtein(u, v) for (u, v) in zip(s, p)))

    return similarity


def noise(s, Q = 3):
    """Randomly changes one random symbol of the given string exactly Q times"""
    for i in range(Q):
        j = random.choice(range(len(s)))
        c = random.choice(string.ascii_lowercase)
        s = s[:j] + c + s[j + 1:]
    return s


def search(s, Q = 2): #old
    ans = list(sorted(data.songs, key = lambda x : song_comparison(s, x)))

    return list(filter(lambda x : song_comparison(s, x) <= Q, ans))


def noisy_comparison(s, t): # s - наш паттерн, t - некоторое слово, посчитать log P(t) + sum log ...
    pass


def top_frequent(s): # взять top сколько-то слов по noisy_comparison(s, word) for word in data.inv
    pass


def full_search(s):
    words = s.split()


res = search("2pac it")
for i in res:
    print(i)

""" K = 4
for i in range(1):
    s = noise(random.choice(data.songs))

    print(s)

    j = 0
    for q in data.songs:
        j += 1
        print(j)
        if song_comparison(s, q) <= K:
            print(q)
"""
