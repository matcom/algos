import os
from itertools import combinations
from math import comb
from collections import Counter

# ----------------------------------------------------------------- model
def lists(n):
    return [("a", i) for i in range(1, n + 1)], [("b", j) for j in range(1, n + 1)]


class Oracle:
    """Answers 'a < b ?' for a front element of A and a front element of B."""
    def __init__(self):
        self.log = []                       # (a, b, a_lt_b) in the order asked

    def a_lt_b(self, a, b):
        r = self._answer(a, b)
        self.log.append((a, b, r))
        return r

    @property
    def count(self):
        return len(self.log)


class AdversaryOracle(Oracle):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def _answer(self, a, b):
        i, j = a[1], b[1]
        return i < j or (i == j == self.n)


class RankOracle(Oracle):
    """A concrete input: rank[x] = position of x in the sorted union."""
    def __init__(self, rank):
        super().__init__()
        self.rank = rank

    def _answer(self, a, b):
        return self.rank[a] < self.rank[b]


def chain_P(n):
    order = []
    for m in range(1, n):
        order += [("b", m), ("a", m)]
    return order + [("a", n), ("b", n)]


def rank_of(order):
    return {x: k for k, x in enumerate(order)}


def standard_merge(A, B, oracle):
    out, i, j = [], 0, 0
    while i < len(A) and j < len(B):
        if oracle.a_lt_b(A[i], B[j]):
            out.append(A[i]); i += 1
        else:
            out.append(B[j]); j += 1
    return out + A[i:] + B[j:]


def optimized_merge(A, B, oracle):
    """Stops comparing as soon as A has ONE element left, dumps B, puts that element last."""
    out, i, j = [], 0, 0
    while len(A) - i > 1 and j < len(B):
        if oracle.a_lt_b(A[i], B[j]):
            out.append(A[i]); i += 1
        else:
            out.append(B[j]); j += 1
    return out + B[j:] + A[i:]


def run(alg, n, oracle):
    A, B = lists(n)
    return alg(A, B, oracle)


def name(x):
    return f"{x[0]}{x[1]}"


# ----------------------------------------------------------------- E1: Adversary
def e1_adversary(N=60):
    print("E1. Adversary against the optimized merge (n = 1..%d)" % N)
    for n in range(1, N + 1):
        P = chain_P(n)
        rank = rank_of(P)
        A, B = lists(n)
        # (a) f is exactly the order of the chain P  -> consistent, a real input exists
        for a in A:
            for b in B:
                assert AdversaryOracle(n)._answer(a, b) == (rank[a] < rank[b]), (n, a, b)
        # (b) optimized merge
        orc = AdversaryOracle(n)
        out = run(optimized_merge, n, orc)
        assert orc.count == max(0, 2 * n - 2), (n, orc.count)
        for k, (a, b, r) in enumerate(orc.log, start=1):          # "extraction lemma"
            m = (k + 1) // 2
            if k % 2 == 1:
                assert (a, b, r) == (("a", m), ("b", m), False)    # a_m vs b_m   -> b_m < a_m
            else:
                assert (a, b, r) == (("a", m), ("b", m + 1), True)  # a_m vs b_{m+1} -> a_m < b_{m+1}
        assert out == P[:-2] + [("b", n), ("a", n)] and out != P   # P with the last two swapped
        # (c) the standard merge pays 2n-1 and is correct on the same adversary
        orc2 = AdversaryOracle(n)
        out2 = run(standard_merge, n, orc2)
        assert orc2.count == 2 * n - 1 and out2 == P
    print("  f == order of P for every (i,j); optimized: exactly 2n-2 questions,")
    print("  output = P with its last two elements swapped (wrong); standard merge: 2n-1, correct. OK")


# ----------------------------------------------------------------- E2: n = 3 example
def e2_example():
    print("\nE2. Example n = 3: A=[2,4,5], B=[1,3,6]")
    n = 3
    P = chain_P(n)
    rank = rank_of(P)
    val = {x: rank[x] + 1 for x in P}
    assert [val[x] for x in lists(n)[0]] == [2, 4, 5] and [val[x] for x in lists(n)[1]] == [1, 3, 6]
    orc = RankOracle(rank)
    out = run(optimized_merge, n, orc)
    for k, (a, b, r) in enumerate(orc.log, start=1):
        print(f"  k={k}: {name(a)}({val[a]}) vs {name(b)}({val[b]}) -> "
              f"{name(a) + ' < ' + name(b) if r else name(b) + ' < ' + name(a)}   "
              f"extracts {name(a) if r else name(b)}({val[a] if r else val[b]})")
    produced = [val[x] for x in out]
    print("  produced:", produced, "  expected:", sorted(produced))
    assert produced == [1, 2, 3, 4, 6, 5]


# ----------------------------------------------------------------- E3: blind spot
def e3_blind_spot(N=40):
    print("\nE3. Blind spot: which A-B pairs that are neighbours in P were never asked")
    for n in range(1, N + 1):
        P = chain_P(n)
        neighbours = {frozenset((P[k], P[k + 1])) for k in range(len(P) - 1) if P[k][0] != P[k + 1][0]}
        assert len(neighbours) == max(0, 2 * n - 2) or n == 1
        orc = AdversaryOracle(n)
        run(optimized_merge, n, orc)
        asked = {frozenset((a, b)) for a, b, _ in orc.log}
        missing = neighbours - asked
        assert missing == {frozenset((("a", n), ("b", n)))}, (n, missing)
        orc2 = AdversaryOracle(n)
        run(standard_merge, n, orc2)
        assert neighbours <= {frozenset((a, b)) for a, b, _ in orc2.log}
    print("  P has 2n-2 cross neighbours (n>=2); optimized skips exactly {a_n, b_n}; standard asks them all. OK")
    print("  (its last question, a_{n-1} vs b_n, is NOT a neighbour pair in P: it is the one 'wasted' question)")


# ----------------------------------------------------------------- E4: indistinguishable inputs
def e4_indistinguishable(N=30):
    print("\nE4. Swapping a_n and b_n (adjacent in P) is invisible to the optimized merge")
    for n in range(1, N + 1):
        P = chain_P(n)
        P2 = P[:-2] + [P[-1], P[-2]]            # ... b_n, a_n   (the input where the shortcut is right)
        o1, o2 = RankOracle(rank_of(P)), RankOracle(rank_of(P2))
        out1, out2 = run(optimized_merge, n, o1), run(optimized_merge, n, o2)
        assert o1.log == o2.log and out1 == out2          # same questions, same answers, same output
        assert out2 == P2 and out1 != P                   # right on P', wrong on P
        s1, s2 = RankOracle(rank_of(P)), RankOracle(rank_of(P2))
        run(standard_merge, n, s1); run(standard_merge, n, s2)
        assert s1.log != s2.log                           # the extra question tells them apart
    print("  same transcript on P and P', same output; correct on P', wrong on P;")
    print("  the standard merge's last question (a_n vs b_n) separates them. OK")


# ----------------------------------------------------------------- E5: exhaustive
def all_inputs(n):
    for ranks_a in combinations(range(2 * n), n):
        sa = set(ranks_a)
        rank = {}
        ia = ib = 0
        for r in range(2 * n):
            if r in sa:
                ia += 1; rank[("a", ia)] = r
            else:
                ib += 1; rank[("b", ib)] = r
        yield rank


def e5_exhaustive(N=10):
    print("\nE5. ALL C(2n,n) inputs (every way to interleave A and B), n = 1..%d" % N)
    print(f"  {'n':>2} {'inputs':>7} {'worst opt':>9} {'2n-2':>5} {'#worst':>7} {'worst std':>9} {'2n-1':>5} "
          f"{'wrong':>7} {'wrong/total':>11}")
    rows, hist = [], {}
    for n in range(1, N + 1):
        wo = ws = 0
        cnt_worst = wrong = total = 0
        h_opt, h_std = Counter(), Counter()
        for rank in all_inputs(n):
            total += 1
            expected = sorted(rank, key=rank.get)
            o = RankOracle(rank); out = run(optimized_merge, n, o)
            s = RankOracle(rank); outs = run(standard_merge, n, s)
            assert outs == expected
            ok = out == expected
            wrong += not ok
            assert ok == (rank[("b", n)] != 2 * n - 1)   # wrong  <=>  the maximum is in B
            wo, ws = max(wo, o.count), max(ws, s.count)
            h_opt[(o.count, ok)] += 1
            h_std[s.count] += 1
        cnt_worst = sum(v for (c, _), v in h_opt.items() if c == wo)
        assert wo == max(0, 2 * n - 2) and ws == 2 * n - 1 and total == comb(2 * n, n) and 2 * wrong == total
        print(f"  {n:>2} {total:>7} {wo:>9} {2 * n - 2:>5} {cnt_worst:>7} {ws:>9} {2 * n - 1:>5} {wrong:>7} "
              f"{wrong / total:>11.3f}")
        rows.append((n, wo, ws, wrong, total))
        hist[n] = (h_opt, h_std)
    print("  worst case of the optimized merge = 2n-2 (no input needs more), standard = 2n-1;")
    print("  it is wrong EXACTLY when the overall maximum belongs to B (a_n < b_n) = half of all inputs. OK")
    return rows, hist


# ----------------------------------------------------------------- E6: random large n
def e6_random(n=1000, trials=3000, seed=9):
    import random
    rng = random.Random(seed)
    print(f"\nE6. {trials} random inputs with n = {n}")
    wrong = worst = 0
    for _ in range(trials):
        ranks_a = set(rng.sample(range(2 * n), n))
        rank, ia, ib = {}, 0, 0
        for r in range(2 * n):
            if r in ranks_a:
                ia += 1; rank[("a", ia)] = r
            else:
                ib += 1; rank[("b", ib)] = r
        expected = sorted(rank, key=rank.get)
        o = RankOracle(rank); out = run(optimized_merge, n, o)
        ok = out == expected
        wrong += not ok
        worst = max(worst, o.count)
        assert o.count <= 2 * n - 2 and ok == (rank[("b", n)] != 2 * n - 1)
    print(f"  max questions seen {worst} (<= 2n-2 = {2 * n - 2}); wrong on {wrong}/{trials} = {wrong / trials:.3f}. OK")



if __name__ == "__main__":
    e1_adversary()
    e2_example()
    e3_blind_spot()
    e4_indistinguishable()
    rows, hist = e5_exhaustive()
    e6_random()
  