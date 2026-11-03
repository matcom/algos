def search_sorted_matrix(matriz, x):
    if not matriz or not matriz[0]:
        return (-1, -1)
    
    n = len(matriz)
    m = len(matriz[0])
    
    i = 0
    j = m - 1
    
    while i < n and j >= 0:
        if matriz[i][j] == x:
            return (i, j)
        elif matriz[i][j] > x:
            j -= 1
        else:
            i += 1
            
    return (-1, -1)