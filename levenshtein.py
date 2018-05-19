import random, string, operator
from itertools import permutations
import functools
from enum import Enum


class Operation(Enum):
    NONE = 0
    ADD = 1
    DELETE = 2
    SUBSTITUTE = 3
    TRANSPOSE = 4
    SINGLE = 5
    DOUBLE = 6


def cost_insert(s):
    """ eps -> s """
    if s == ' ': return 0
    return 1


def cost_delete(s):
    """ s -> eps """
    if s == ' ': return 0
    return 1


def cost_transpose(s, t):
    """ st -> ts """
    return 1


def cost_subst(s, t):
    """ s -> t """
    if s == t: return 0
    return 1


def cost_double(s):
    """ a -> aa """
    return 0


def cost_single(s):
    """ aa -> a """
    return 0


def lightweight_lvs(s, t):
    n, m = len(s), len(t)
    dp = [[10 ** 9 for _ in range(m + 1)] for _ in range(n + 1)]

    dp[0][0] = 0

    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + cost_delete(s[i - 1])
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + cost_insert(t[j - 1])

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            res = [dp[i - 1][j] + cost_delete(s[i - 1]),
                   dp[i][j - 1] + cost_insert(t[j - 1]),
                   dp[i - 1][j - 1] + cost_subst(s[i - 1], t[j - 1])]
            dp[i][j] = min(res)

    return dp[-1][-1]


def levenshtein(s, t, mode = False):
    n, m = len(s), len(t)
    dp = [[[10 ** 9, Operation.NONE] for _ in range(m + 1)] for _ in range(n + 1)]

    dp[0][0] = [0, Operation.NONE]

    for i in range(1, n + 1):
        dp[i][0] = [dp[i - 1][0][0] + cost_delete(s[i - 1]), Operation.DELETE]
    for j in range(1, m + 1):
        dp[0][j] = [dp[0][j - 1][0] + cost_insert(t[j - 1]), Operation.ADD]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            results = [
                [dp[i - 1][j - 1][0] + cost_subst(s[i - 1], t[j - 1]), Operation.SUBSTITUTE, s[i - 1], t[j - 1]],
                [dp[i - 1][j][0] + cost_delete(s[i - 1]), Operation.DELETE, s[i - 2] + s[i - 1] if i > 1 else s[i - 1], s[i - 2] if i > 1 else ''],
                [dp[i][j - 1][0] + cost_insert(t[j - 1]), Operation.ADD, t[j - 2] if j > 1 else '', t[j - 2] + t[j - 1] if j > 1 else t[j - 1]],
                #[dp[i - 1][j - 1][0] + cost_subst(s[i - 1], t[j - 1]), Operation.SUBSTITUTE, s[i - 1], t[j - 1]],
                [dp[i - 2][j - 2][0] + cost_transpose(s[i - 1], t[j - 1]), Operation.TRANSPOSE, s[i - 1], t[j - 1]]
                if i > 1 and j > 1 and s[i - 1] == t[j - 2] and s[i - 2] == t[j - 1] else [10 ** 9],
                [dp[i - 2][j - 1][0] + cost_single(s[i - 1]), Operation.SINGLE, s[i - 1]]
                if len(s) > 1 and s[i - 1] == t[j - 1] and s[i - 2] == s[i - 1] else [10 ** 9],
                [dp[i - 2][j - 1][0] + cost_double(s[i - 1]), Operation.DOUBLE, s[i - 1]]
                if len(t) > 1 and s[i - 1] == t[j - 1] and t[j - 2] == t[j - 1] else [10 ** 9]
            ]

            dp[i][j] = min(results, key = lambda x : x[0])

    if not mode:
        return dp[-1][-1][0]

    x, y = len(s), len(t)

    backtrace = []

    while x >= 1 and y >= 1:
        #print(x, y)
        #print(dp[x][y])
        try:
            op_type = dp[x][y][1]
            #print(op_type)
            if op_type == Operation.NONE:
                assert False
            elif op_type == Operation.ADD:
                u, v = dp[x][y][-2:]
                backtrace.append([op_type, u + '->' + v])
                y -= 1
            elif op_type == Operation.DELETE:
                u, v = dp[x][y][-2:]
                backtrace.append([op_type, u + '->' + v])
                x -= 1
            elif op_type == Operation.SUBSTITUTE:
                u, v = dp[x][y][-2:]
                if u != v:
                    backtrace.append([op_type, u + '->' + v])
                x, y = x - 1, y - 1
            elif op_type == Operation.TRANSPOSE:
                u, v = dp[x][y][-2:]
                backtrace.append([op_type, u + v + '->' + v + u])
                x, y = x - 2, y - 2
            elif op_type == Operation.SINGLE:
                backtrace.append([op_type, dp[x][y][-1] * 2 + '->' + dp[x][y][-1]])
                x, y = x - 2, y - 1
            elif op_type == Operation.DOUBLE:
                backtrace.append([op_type, dp[x][y][-1] + '->' + dp[x][y][-1] * 2])
                x, y = x - 1, y - 2
        except IndexError as e:
            print('Aaaaa blyadddddddddddddddd')
            assert 0

    backtrace = backtrace[::-1]

    #print(backtrace)

    return dp[-1][-1][0], backtrace


def min_weight_max_matching(n, m, cost_array):
    arr = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(n):
        for j in range(m):
            arr[i + 1][j + 1] = cost_array[i][j]

    u = [0 for i in range(n + 1)]
    v = [0 for i in range(m + 1)]
    p = [0 for i in range(m + 1)]
    way = [0 for i in range(m + 1)]

    for i in range(1, n + 1):
        p[0] = i
        q = 0

        minv = [10 ** 9 for _ in range(m + 1)]
        used = [0 for _ in range(m + 1)]

        while True:
            used[q] = 1
            k, delta = p[q], 10 ** 9
            J = -1
            for j in range(1, m + 1):
                if not used[j]:
                    curr = arr[k][j] - u[k] - v[j]
                    if curr < minv[j]:
                        minv[j], way[j] = curr, q
                    if minv[j] < delta:
                        delta, J = minv[j], j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            q = J
            if not p[q]: break

        while True:
            J = way[q]
            p[q] = p[J]
            q = J
            if not q: break

    return -v[0]