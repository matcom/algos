def find_missing_number(A):
    n = len(A)
    expected_sum = (n + 1) * (n + 2) // 2
    actual_sum = 0
    
    for num in A:
        actual_sum += num
        
    return expected_sum - actual_sum


if __name__ == "__main__":
    test_cases = [
        ([1, 2, 4, 5], 3),
        ([2, 3, 4, 5], 1),
        ([1, 2, 3, 4], 5),
        ([1], 2),
        ([], 1)
    ]
    
    for A, expected in test_cases:
        result = find_missing_number(A)
        assert result == expected, f"Failed for {A}: expected {expected}, got {result}"
        print(f"Array: {A} -> Missing: {result}")