"""
Guarded Matrix Search Implementation.

Verifies:
1. Loop Invariant: If target `x` is in matrix A, it must remain in active region A[i..n-1][0..j].
2. Potential Function: Phi = (n - i) + (j + 1) >= 2 during loop, decreasing by exactly 1 per step.
3. Worst-Case Bound: Total comparisons <= 2n - 1.
"""

def contains_oracle(matrix, target):
    """Brute-force oracle to determine if target exists anywhere in the matrix."""
    return any(target in row for row in matrix)


def find_x_guarded(matrix, target):
    """
    Searches for `target` in an N x N matrix with sorted rows and columns.
    Enforces invariant, potential, and complexity bounds using assertions.
    
    Returns:
        tuple: (found: bool, comparisons: int)
    """
    n = len(matrix)
    i, j = 0, n - 1
    
    # Ground truth check using brute-force oracle
    target_exists = contains_oracle(matrix, target)
    
    # Initial potential: Phi = (n - i) + (j + 1) = n + n = 2n
    phi = (n - i) + (j + 1)
    assert phi == 2 * n, f"Initial potential must be 2n, got {phi}"
    
    comparisons = 0

    while i < n and j >= 0:
        # ------------------------------------------------------------------
        # 1. INVARIANT CHECK
        # If target exists, it MUST be in the active region A[i..n-1][0..j]
        # ------------------------------------------------------------------
        if target_exists:
            active_region = [matrix[r][c] for r in range(i, n) for c in range(0, j + 1)]
            assert target in active_region, (
                f"INVARIANT VIOLATED at (i={i}, j={j}): "
                f"target {target} was incorrectly discarded!"
            )
        
        # ------------------------------------------------------------------
        # 2. POTENTIAL LOWER BOUND CHECK
        # While loop guard is True (i < n and j >= 0), phi must be >= 2
        # ------------------------------------------------------------------
        assert phi >= 2, f"POTENTIAL ERROR: phi dropped below 2 while loop is active (phi={phi})"

        # Perform comparison with top-right element of active subgrid
        comparisons += 1
        current_val = matrix[i][j]

        if current_val == target:
            # Target found
            assert target_exists, "Algorithm reported True, but oracle says target does not exist"
            assert comparisons <= 2 * n - 1, f"Exceeded comparison bound: {comparisons} > {2*n - 1}"
            return True, comparisons
            
        elif current_val > target:
            # Current element > target: discard column j
            j -= 1
        else:
            # Current element < target: discard row i
            i += 1

        # ------------------------------------------------------------------
        # 3. POTENTIAL DECREASE CHECK
        # Phi must decrease by EXACTLY 1 unit per iteration
        # ------------------------------------------------------------------
        new_phi = (n - i) + (j + 1)
        assert new_phi == phi - 1, f"POTENTIAL ERROR: phi did not decrease by 1 ({phi} -> {new_phi})"
        phi = new_phi

    # ----------------------------------------------------------------------
    # 4. CONCLUSION & TERMINATION CHECK
    # Active region is empty (i == n or j == -1)
    # ----------------------------------------------------------------------
    assert i == n or j == -1, f"Terminated at invalid indices: (i={i}, j={j})"
    assert not target_exists, "Active region is empty, but target exists in matrix (Invariant Failure)"
    assert comparisons <= 2 * n - 1, f"Exceeded comparison bound: {comparisons} > {2*n - 1}"

    return False, comparisons


def run_tests():
    """Runs a test suite across various matrices and targets."""
    sample_matrix = [
        [ 1,  4,  7, 11, 15],
        [ 2,  5,  8, 12, 19],
        [ 3,  6,  9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ]
    
    n = len(sample_matrix)
    print(f"--- Running Guarded Search Tests (N = {n}) ---")

    # Test cases: (target, expected_result)
    test_cases = [
        (5, True),     # Center element
        (1, True),     # Top-left (minimum)
        (30, True),    # Bottom-right (maximum)
        (15, True),    # Top-right (first check)
        (18, True),    # Bottom-left
        (14, True),    # Interior element
        (20, False),   # Absent element (in-between)
        (0, False),    # Absent element (smaller than min)
        (35, False),   # Absent element (larger than max)
    ]

    for target, expected in test_cases:
        found, comps = find_x_guarded(sample_matrix, target)
        assert found == expected, f"Failed for target={target}: expected {expected}, got {found}"
        print(f"Target {target:>2d}: Found={str(found):<5s} | Comparisons={comps:>2d}/{2*n-1} [PASSED]")

    print("\nAll assertions passed successfully! Invariant, Potential, and Complexity verified.")


if __name__ == "__main__":
    run_tests()
