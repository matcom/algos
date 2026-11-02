"""
Executable Invariant Verification for Exercise 8.
"""

import sys
from collections import Counter
from typing import List, Any, Tuple, Dict
from solution import first_pass

# Invariant Verification Functions

def can_partition_into_triplets(s: List[Any]) -> bool:
    """
    Lemma 2: A multiset S partitions into triplets of distinct elements if and only if
    |S| is a multiple of 3 and no element occurs more than |S| / 3 times.
    """
    n = len(s)
    if n % 3 != 0:
        return False
    if n == 0:
        return True

    counts = Counter(s)
    return all(3 * cnt <= n for cnt in counts.values())

def invariant_holds(prefix: List[Any], cand1: Any, count1: int, cand2: Any, count2: int) -> bool:
    """
    Checks if invariants (I1), (I2), and (I3) hold for a prefix and current candidate state.
    """
    # (I2) Non-negative counts
    if count1 < 0 or count2 < 0:
        return False

    # (I3) Active candidates must be distinct
    if count1 > 0 and count2 > 0 and cand1 == cand2:
        return False

    # (I1) Subtract active copies from prefix, then check if remaining multiset partitions into triplets
    remainder = Counter(prefix)
    if count1 > 0:
        if remainder[cand1] < count1:
            return False  # Prefix contains fewer copies than claimed by count1
        remainder[cand1] -= count1

    if count2 > 0:
        if remainder[cand2] < count2:
            return False  # Prefix contains fewer copies than claimed by count2
        remainder[cand2] -= count2

    # Verify remainder partitions into triplets
    return can_partition_into_triplets(list(remainder.elements()))


def monitored_first_pass(arr: List[Any]) -> Tuple[Any, int, Any, int]:
    """
    Executes verification by calling solution's first_pass on every prefix arr[:i+1].
    Reuses first_pass directly without duplicating the loop or branch logic!
    """
    base_state = first_pass([])
    assert invariant_holds([], *base_state), "Invariant failed at base case (i = 0)"

    for i in range(len(arr)):
        prefix = arr[:i + 1]
        state = first_pass(prefix)
        assert invariant_holds(prefix, *state), f"Invariant failed at prefix {prefix}, state={state}"

    return first_pass(arr)


# Exhaustive Verification via Canonical Prefixes

def run_exhaustive_verification(max_len: int) -> Tuple[int, Dict[int, int]]:
    """
    Traverses the tree of all canonical prefixes up to length max_len.
    Canonical form: first unseen symbol is 0, second is 1, etc.
    Returns (total_nodes, branch_counts_by_case).
    """
    total_nodes = 0
    case_counts = Counter()

    def determine_case(cand1: Any, count1: int, cand2: Any, count2: int, x: Any) -> int:
        if x == cand1:
            return 1
        if x == cand2:
            return 2
        if count1 == 0:
            return 3
        if count2 == 0:
            return 4
        return 5

    prefix = []

    def dfs(state: Tuple[Any, int, Any, int], max_used_symbol: int):
        nonlocal total_nodes
        total_nodes += 1

        if len(prefix) == max_len:
            return

        cand1, count1, cand2, count2 = state
        for x in range(max_used_symbol + 1):
            case_num = determine_case(cand1, count1, cand2, count2, x)
            case_counts[case_num] += 1

            # Get next state by calling first_pass on the new prefix
            prefix.append(x)
            next_state = first_pass(prefix)

            assert invariant_holds(prefix, *next_state), f"Invariant failed at prefix {prefix}, state={next_state}"
            dfs(next_state, max(max_used_symbol, x + 1))
            prefix.pop()

    initial_state = first_pass([])
    assert invariant_holds([], *initial_state)
    dfs(initial_state, 0)

    return total_nodes, dict(sorted(case_counts.items()))


# Main Test Runner

if __name__ == "__main__":
    print("\n--- Canonical Exhaustive Search ---")
    max_length = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    nodes, branch_summary = run_exhaustive_verification(max_length)
    print(f"Exhaustive search up to length {max_length}: invariant holds across {nodes - 1} distinct canonical prefixes.")
    print("Branch executions per case:", branch_summary)

    print("\nAll tests and invariant checks passed successfully!")

