def boyer_moore_n3_unverified(A):
    c1, c2 = None, None
    k1, k2 = 0, 0
    for x in A:
        if x == c1:
            k1 += 1
        elif x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:
            k1 -= 1
            k2 -= 1
            
    candidates = []
    if k1 > 0 and c1 is not None:
        candidates.append(c1)
    if k2 > 0 and c2 is not None:
        candidates.append(c2)
    return candidates