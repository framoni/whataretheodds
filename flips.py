"""

Karen flips N fair coins. Becky flips N+1 fair coins.
What's the probability for Becky to get more heads than Karen?
Compute it for an arbitary large N.

"""

from itertools import permutations
import numpy as np
import pandas as pd
import seaborn as sns


def probs_head(N):
    base_prob = (1/2)**N
    P = []
    for num_heads in range(0, N+1):
        pattern = [1] * num_heads + [0] * (N - num_heads)
        P.append(base_prob * len(set(permutations(pattern))))
    return P


def probs_players(N, delta, mode):
    P_K = probs_head(N)
    P_B = probs_head(N + delta)
    p_B_over_K = 0
    if mode == "equal":
        for i in range(len(P_K)):
            p_B_over_K += P_K[i] * P_B[i]
    elif mode == "more":
        for i in range(len(P_K)):
            p_B_over_K += P_K[i] * (sum(P_B[i+1:]))
    elif mode == "less":
        for i in range(len(P_K)):
            p_B_over_K += P_K[i] * (sum(P_B[:i]))
    return p_B_over_K


def build_df(M, mode):
    z = np.zeros([M, M])
    for i in range(1, M + 1):
        v = []
        for j in range(0, M - i + 1):
            v.append(probs_players(i, j, mode))
        z[i - 1, i - 1:M] = v
    df = pd.DataFrame(z)
    df.index = np.arange(1, len(df) + 1)
    df.columns = pd.RangeIndex(1, len(df.columns) + 1)
    cm = sns.cubehelix_palette(8, start=.5, rot=-.75, as_cmap=True)
    htm = df.style.background_gradient(cmap=cm, axis=None).render()
    return htm


if __name__ == "__main__":
    M = input("Size? ")
    M = int(M)
    htm_equal = build_df(M, "equal")
    htm_more = build_df(M, "more")
    htm_less = build_df(M, "less")
    htm = "<h2>Probability that Player 1 with COL flips gets more heads than Player 2 with ROW flips</h2><br>" + \
          htm_more + "<h2>Probability that Player 1 with COL flips gets equal number of heads as Player 2 with ROW flips</h2><br>" \
          + htm_equal + "<h2>Probability that Player 1 with COL flips gets less heads than Player 2 with ROW flips</h2><br>" + \
          htm_less
    with open("output/flips_{}.htm".format(M), "w") as f:
        f.write(htm)
