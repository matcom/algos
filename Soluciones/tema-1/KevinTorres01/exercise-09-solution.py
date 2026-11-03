def buggy_merge(A, B):
    n = len(A)
    res = []
    i, j = 0, 0
    
    while i < n - 1 and j < n:
        if A[i] <= B[j]:
            res.append(A[i])
            i += 1
        else:
            res.append(B[j])
            j += 1
            
    if i == n - 1:
        res.append(A[i])
        while j < n:
            res.append(B[j])
            j += 1
    else:
        while i < n:
            res.append(A[i])
            i += 1
        while j < n:
            res.append(B[j])
            j += 1
            
    return res

if __name__ == "__main__":
    A = [1, 2, 4]
    B = [3, 5, 6]
    print("Algoritmo:", buggy_merge(A, B))
    print("Esperado: ", sorted(A + B))