def binary_search(A, x):
    low = 0
    high = len(A) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if A[mid] == x:
            return (mid, True)
        elif A[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
            
    return (low, False)


if __name__ == "__main__":
    A = [1, 3, 5, 7, 9]
    tests = [5, 3, 9, 1, 4, 10]
    
    for x in tests:
        index, found = binary_search(A, x)
        if found:
            print(f"Found {x} at index {index}")
        else:
            print(f"{x} not found. Insertion point: {index}")