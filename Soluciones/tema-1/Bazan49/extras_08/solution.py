from typing import List, Any

def first_pass(arr: List[Any]):
    """
    First pass: cancels triplets of distinct elements.
    Returns the two potential candidates and their remaining counts.
    """
    cand1, count1 = None, 0
    cand2, count2 = None, 0

    for x in arr:
        if x == cand1:
            count1 += 1
        elif x == cand2:
            count2 += 1
        elif count1 == 0:
            cand1, count1 = x, 1
        elif count2 == 0:
            cand2, count2 = x, 1
        else:
            count1 -= 1
            count2 -= 1

    return cand1, count1, cand2, count2


def solution(arr: List[Any]) -> List[Any]:
    """
    Returns all elements appearing strictly more than n / 3 times in O(n) time and O(1) space.
    """
    n = len(arr)
    if n == 0:
        return []

    # First pass: Candidate selection via triplet cancellation
    cand1, count1, cand2, count2 = first_pass(arr)

    # Second pass: Exact verification of candidates with positive counts
    result = []
    for cand, count in [(cand1, count1), (cand2, count2)]:
        if count > 0 and 3 * arr.count(cand) > n:
            result.append(cand)

    return result