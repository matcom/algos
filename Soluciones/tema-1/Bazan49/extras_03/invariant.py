"""
Verification of the MinStack Invariant 

This module implements:
1. MinStack: A O(1) minimum stack storing (value, min_so_far) pairs.
2. Oracle: An abstract reference stack for ground truth comparison.
3. Invariant Checker: Programmatic validation of Invariant.
4. Monitor & Test Suite: Exhaustive and randomized test coverage.
"""

import itertools
import random
import time
from solution import MinStack;


# 1. DATA STRUCTURES

class Oracle:
    """An abstract reference stack implementation used as the ground truth."""

    def __init__(self):
        self.elements = []

    def push(self, val: int) -> None:
        self.elements.append(val)

    def pop(self) -> int | None:
        if self.elements:
            return self.elements.pop()
        return None

    def top(self) -> int | None:
        return self.elements[-1] if self.elements else None

    def min(self) -> int | None:
        return min(self.elements) if self.elements else None

    def __len__(self) -> int:
        return len(self.elements)


# 2. INVARIANT VERIFICATION

def get_stack_pairs(stack: MinStack) -> list[tuple[int, int]]:
    """Extracts the internal (value, min) pairs from bottom to top."""
    return list(stack._stack)


def check_invariant_J(stack: MinStack, abstract_sequence: list[int]) -> bool:
    """
    Validates Invariant:
    1. |S| = |X|
    2. For every level i in {0..n-1}: S[i] == (X[i], min(X[0..i]))
    """
    pairs = get_stack_pairs(stack)

    # Property 1: Size synchronization
    if len(pairs) != len(abstract_sequence):
        return False

    # Property 2: Inductive prefix minimum
    running_min = None
    for i, val in enumerate(abstract_sequence):
        running_min = val if i == 0 else min(running_min, val)
        if pairs[i] != (val, running_min):
            return False

    return True


def monitor(stack: MinStack, oracle: Oracle) -> bool:
    """
    Checks that all external observations match the oracle AND
    that Invariant holds strictly for the internal representation.
    """
    observations_match = (
        len(stack) == len(oracle)
        and stack.top() == oracle.top()
        and stack.min() == oracle.min()
    )
    invariant_holds = check_invariant_J(stack, oracle.elements)

    return observations_match and invariant_holds


# 3. TEST SUITE


def run_single_sequence(ops: list[tuple[str, int] | tuple[str]]) -> bool:
    """Executes a sequence of operations while validating Invariant after each step."""
    stack = MinStack()
    oracle = Oracle()

    if not monitor(stack, oracle):
        return False

    for op in ops:
        if op[0] == "push":
            stack.push(op[1])
            oracle.push(op[1])
        elif op[0] == "pop":
            stack.pop()
            oracle.pop()

        if not monitor(stack, oracle):
            return False

    return True


def test_exhaustive(max_depth: int = 9, values: tuple[int, ...] = (1, 2, 3)):
    """Runs exhaustive search over all operation sequences up to max_depth."""
    print(
        f"--- Running Exhaustive Test (depth <= {max_depth}, values = {values}) ---"
    )
    op_choices = [("push", v) for v in values] + [("pop",)]
    total_checked = 0

    for depth in range(1, max_depth + 1):
        for ops in itertools.product(op_choices, repeat=depth):
            total_checked += 1
            success = run_single_sequence(list(ops))
            assert (
                success
            ), f"Invariant violated on sequence: {ops}"

    print(
        f"[OK] Successfully verified {total_checked} operation prefixes. 0 failures.\n"
    )


def test_randomized(num_trials: int = 2000, max_ops: int = 200):
    """Runs randomized sequences of varying length, ratios, and value ranges."""
    print(f"--- Running Randomized Test ({num_trials} trials) ---")
    random.seed(7)
    total_ops = 0

    for _ in range(num_trials):
        ops_count = random.randint(1, max_ops)
        push_bias = random.choice([0.3, 0.5, 0.7])
        val_range = random.choice([2, 5, 1000])

        ops = []
        for _ in range(ops_count):
            if random.random() < push_bias:
                ops.append(("push", random.randrange(val_range)))
            else:
                ops.append(("pop",))

        total_ops += len(ops)
        success = run_single_sequence(ops)
        assert (
            success
        ), f"Invariant violated on randomized sequence: {ops}"

    print(
        f"[OK] Successfully verified {num_trials} trials ({total_ops} total operations). 0 failures.\n"
    )


# MAIN EXECUTION

if __name__ == "__main__":
    start_time = time.time()
    print("   STARTING INVARIANT VERIFICATION SUITE      \n")

    test_exhaustive(max_depth=9, values=(1, 2, 3))
    test_randomized(num_trials=2000, max_ops=200)

    elapsed = time.time() - start_time
    print(f"All tests passed successfully in {elapsed:.2f} seconds.")