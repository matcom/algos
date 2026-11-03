def find_x(A,x):
    n = len(A)
    i, j = 0, n - 1

    while(i < n and j >= 0):
        if(A[i][j] == x):
            return True
        elif(A[i][j] > x):
            j -= 1
        else:
            i += 1

    return False
