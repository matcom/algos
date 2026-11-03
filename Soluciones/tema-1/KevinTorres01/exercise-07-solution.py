def find_median_sorted_arrays(A, B):
    n = len(A)
    if n > len(B):
        A, B = B, A
        n = len(A)
        
    m = len(B)
    start, end = 0, n
    
    while start <= end:
        i = (start + end) // 2
        j = (n + m + 1) // 2 - i
        
        max_left_A = A[i - 1] if i > 0 else float('-inf')
        max_left_B = B[j - 1] if j > 0 else float('-inf')
        
        min_right_A = A[i] if i < n else float('inf')
        min_right_B = B[j] if j < m else float('inf')
        
        if max_left_A <= min_right_B and max_left_B <= min_right_A:
            return max(max_left_A, max_left_B)
            
        elif max_left_A > min_right_B:
            end = i - 1
        else:
            start = i + 1
