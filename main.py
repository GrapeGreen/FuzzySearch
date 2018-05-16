import data, random, string
from itertools import permutations

def cost_insert(s):
    return 1


def cost_delete(s):
    return 1


def cost_swap(s, t):
    return 1


def cost_subst(s, t):
    return 1 if s != t else 0


def levenshtein(s, t):
    n, m = len(s), len(t)
    dp = [[10 ** 9 for j in range(m + 1)] for i in range(n + 1)]

    dp[0][0] = 0

    for i in range(m + 1):
        dp[0][i] = i
    for j in range(n + 1):
        dp[j][0] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            x = min(dp[i - 1][j] + cost_insert(s[i - 1]), dp[i][j - 1] + cost_delete(t[j - 1]))
            x = min(x, dp[i - 1][j - 1] + cost_subst(s[i - 1], t[j - 1]))
            if i > 1 and j > 1 and s[i - 1] == t[j - 2] and s[i - 2] == t[j - 1]:
                x = min(x, dp[i - 2][j - 2] + cost_swap(s[i - 1], t[j - 1]))

            # TODO: aa -> a & a -> aa

            dp[i][j] = x

    return dp[len(s)][len(t)]


def song_comparison(s, t): 
    """n = len(s), m = len(t), n < m -> among all A(m, n) combinations we choose minimal \
    by sum of corresponding Levenshtein distances"""

    # Warning: too slow :(

    s, t = s.split(), t.split()
    similarity = 10 ** 9
    if len(s) > len(t):
        s, t = t, s
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

