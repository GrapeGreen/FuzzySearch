import data, mistakes
from numpy import log
from levenshtein import levenshtein, lightweight_lvs


# time for some MAGIC!
FREQUENCY_REDUCTION = 1 / 10 ** 6
ZERO_PROBABILITY = 1 / 10 ** 12
TOP = 30

def calculate_all(s, Q = 2):
    probs = [x for x in data.inv if abs(len(x) - len(s)) <= Q and lightweight_lvs(s, x) <= Q + 1]
    probs.sort(key=lambda x: calculate_probs(s, x), reverse=True)

    leftover = probs if len(probs) <= TOP else probs[:TOP]
    print('debug : ', leftover)
    return leftover


def calculate_probs(s, t):
    dist, ops = levenshtein(s, t, True)
    op_types = []
    symbs = []

    for j in ops:
        op_types.append(j[0])
        symbs.append(j[1])
    probs = log(data.d[t] * FREQUENCY_REDUCTION)

    for i in range(len(symbs)):
        sym1, sym2 = symbs[i].split("->")
        if (sym1, sym2) in mistakes.types[op_types[i]]:
            probs += log(mistakes.types[op_types[i]][(sym1, sym2)] / mistakes.c[(sym1, sym2)])
        else:
            probs += log(ZERO_PROBABILITY)

    return probs