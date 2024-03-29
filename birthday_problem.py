from math import prod
import matplotlib.pyplot as plt
from sympy.utilities.iterables import multiset_partitions
from tqdm import tqdm


def at_least_2(N):
    """
    Compute the probability that at least 2 of N people share their birthday.
    1. Calculate all partitions of the set {1, ..., N}, excluding the one made only by singlets
    2. For each partition of length L, we have 365*364*...*(365-(L-1)) choices
    3. Sum all the choices for each partition ---> num
    4. Divide by all possible configurations  365^N ---> dem
    """

    num = 0
    for i in multiset_partitions(N):
        if len(i) < N:
            Pi = prod([365 - j for j in range(len(i))])
            num += Pi
    den = pow(365, N)
    return num / den


def at_least_k(k, N):
    """
    Compute the probability that at least k of N people share their birthday.
    1. Calculate all partitions of the set {1, ..., N}, excluding the ones that only have subsets with less thank k items
    2. For each partition of length L, we have 365*364*...*(365-(L-1)) choices
    3. Sum all the choices for each partition ---> num
    4. Divide by all possible configurations  365^N ---> dem
    """

    num = 0
    for i in multiset_partitions(N):
        if all([len(s) < k for s in i]):
            continue
        else:
            Pi = prod([365 - j for j in range(len(i))])
            num += Pi
    den = pow(365, N)
    return num / den


if __name__ == '__main__':
    max = 100
    P = []
    k = 2
    for i in tqdm(range(k, max+1)):
        P.append(at_least_k(k, i))
    plt.figure()
    plt.plot(list(range(2, max+1)), P)
    plt.savefig('output/birthday_problem_{}_{}.png'.format(k, max))
