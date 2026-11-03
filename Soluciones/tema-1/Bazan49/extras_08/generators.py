"""
Generators and Shortcut Analysis for Exercise 8.
Executes Table A, Table B, Table C, and Stress Test matching the original source code,
and writes the output to a .txt file.
"""

import itertools
import math
import random
from collections import Counter
from typing import List, Any
from solution import solution, first_pass

ALPHABET = "ABCDE"


# ------------------------------------------------------------------ Core functions
def shortcut_solution(arr: List[Any]) -> List[Any]:
    """INCORRECT SHORTCUT: returns candidates with count > 0 without second pass."""
    cand1, count1, cand2, count2 = first_pass(arr)
    return [cand for cand, count in [(cand1, count1), (cand2, count2)] if count > 0]


def oracle(arr: List[Any]) -> List[Any]:
    """Ground truth oracle: returns all elements appearing strictly more than n / 3 times."""
    n = len(arr)
    counts = Counter(arr)
    return [item for item, cnt in counts.items() if 3 * cnt > n]


# ------------------------------------------------------------------ Generators
def planted_one(n: int) -> List[Any]:
    """One planted majority (> n/3) and remaining elements at random."""
    m = random.choice(ALPHABET)
    q = n // 3 + 1
    arr = [m] * q + [random.choice(ALPHABET) for _ in range(n - q)]
    random.shuffle(arr)
    return arr


def planted_two(n: int) -> List[Any]:
    """Two planted majorities (> n/3 each); remaining elements at random. Requires n >= 4."""
    if n < 4:
        n = 4
    a, b = random.sample(ALPHABET, 2)
    q = n // 3 + 1
    arr = [a] * q + [b] * q + [random.choice(ALPHABET) for _ in range(max(0, n - 2 * q))]
    random.shuffle(arr)
    return arr


def balanced_ternary(n: int) -> List[Any]:
    """Three symbols with exactly n//3 copies each (length = 3 * (n // 3)), shuffled."""
    m = n // 3
    arr = ["A"] * m + ["B"] * m + ["C"] * m
    random.shuffle(arr)
    return arr


def binary_random(n: int) -> List[Any]:
    """Random binary array of 'A' and 'B'."""
    return [random.choice("AB") for _ in range(n)]


def three_symbols(n: int) -> List[Any]:
    """Random array of 'A', 'B', 'C'."""
    return [random.choice("ABC") for _ in range(n)]


def five_symbols(n: int) -> List[Any]:
    """Random array of 'A', 'B', 'C', 'D', 'E'."""
    return [random.choice("ABCDE") for _ in range(n)]


GENERATORS = {
    "planted 1 majority": planted_one,
    "planted 2 majorities": planted_two,
    "balanced ternary": balanced_ternary,
    "binary": binary_random,
    "3 symbols": three_symbols,
    "5 symbols": five_symbols,
}


def failure_rate(generator_fn, lengths: List[int], num_samples: int, solver_fn) -> float:
    """Fraction of arrays where solver_fn output differs from oracle."""
    failures = 0
    for _ in range(num_samples):
        length = random.choice(lengths)
        arr = generator_fn(length)
        if sorted(solver_fn(arr)) != sorted(oracle(arr)):
            failures += 1
    return failures / num_samples


def exact_binary_error(n: int) -> float:
    """Exact P(shortcut fails) on uniform binary arrays of length n."""
    wrong = 0
    for k in range(n + 1):
        if (1 <= k and 3 * k <= n) or (1 <= n - k and 3 * (n - k) <= n):
            wrong += math.comb(n, k)
    return wrong / (2 ** n)


def run_all_experiments() -> str:
    lines = []
    
    # ---------------------------------------------------- Table A
    random.seed(5)
    lengths_A = list(range(4, 16))
    lines.append("== Table A: % of arrays where each version fails (lengths 4..15, 4000 samples) ==")
    lines.append(f"{'generator':>24} {'shortcut':>10} {'two passes':>12}")
    
    for name, gen in GENERATORS.items():
        err_shortcut = failure_rate(gen, lengths_A, 4000, shortcut_solution)
        err_solution = failure_rate(gen, lengths_A, 4000, solution)
        lines.append(f"{name:>24} {100 * err_shortcut:9.1f}% {100 * err_solution:11.1f}%")
        
    # ---------------------------------------------------- Table B
    lines.append("\n== Table B: % of shortcut failures by array length n (2000 samples per cell) ==")
    ns = (6, 10, 15, 30, 60, 100, 300)
    lines.append(f"{'generator':>24} " + " ".join(f"{'n=' + str(n):>7}" for n in ns))
    
    for name, gen in GENERATORS.items():
        cells = [100 * failure_rate(gen, [n], 2000, shortcut_solution) for n in ns]
        lines.append(f"{name:>24} " + " ".join(f"{c:6.1f}%" for c in cells))
        
    exact_b = [100 * exact_binary_error(n) for n in ns]
    lines.append(f"{'binary (exact)':>24} " + " ".join(f"{c:6.1f}%" for c in exact_b))

    # ---------------------------------------------------- Table C
    lines.append("\n== Table C: shortcut error by number of majority elements (|H|) ==")
    lines.append("   (all arrays over ABCDE of length 1..8)")
    
    counts_by_h = {0: [0, 0], 1: [0, 0], 2: [0, 0]}
    omissions = 0
    
    for L in range(1, 9):
        for tup in itertools.product(ALPHABET, repeat=L):
            arr = list(tup)
            H = set(oracle(arr))
            S = set(shortcut_solution(arr))
            counts_by_h[len(H)][0] += 1
            counts_by_h[len(H)][1] += (S != H)
            if not H.issubset(S):
                omissions += 1
                
    for h, (tot, wrong) in counts_by_h.items():
        lines.append(f"   |H| = {h}: {tot:>7} arrays, shortcut fails in {wrong:>7} ({100 * wrong / tot:5.1f}%)")
    lines.append(f"   omissions (majority element not returned by shortcut): {omissions}")

    # ---------------------------------------------------- Stress Test
    lines.append("\n== Stress test: 200,000 arrays of 2 planted majorities, n up to 300 ==")
    random.seed(11)
    failures_stress = 0
    for _ in range(200_000):
        arr = planted_two(random.randint(4, 300))
        if sorted(shortcut_solution(arr)) != sorted(oracle(arr)):
            failures_stress += 1
            
    lines.append(f"   shortcut failed in {failures_stress} out of 200,000 arrays")
    
    return "\n".join(lines)


if __name__ == "__main__":
    output_text = run_all_experiments()
    print(output_text)
    
    # Save output to text file
    with open("generators_output.txt", "w", encoding="utf-8") as f:
        f.write(output_text)

