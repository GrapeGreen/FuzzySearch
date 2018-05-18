import data, mistakes
from numpy import log
from levenshtein import levenshtein
from collections import namedtuple

# time for some MAGIC!
FREQUENCY_REDUCTION = 1 / 10 ** 4
ZERO_PROBABILITY = 1 / 10 ** 12


def laplas_smooth(fr_f, type):
    type_fr = sum(mistakes.types[type].values())
    unique_mistakes = len(mistakes.types[type])

    return (fr_f + 1) / (type_fr + unique_mistakes)


def calculate_all(s):
    probs = [x for x in data.inv if abs(len(x) - len(s)) <= 1]
    probs.sort(key=lambda x: calculate_probs(s, x), reverse=True)

    return probs[:10]


def calculate_probs(s, t):
    ops = levenshtein(s, t, True)

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


s = input()
res = calculate_all(s)

for word in res:
    print(word, calculate_probs(s, word))