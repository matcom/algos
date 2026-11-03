import random

def closest_pair_1d(points, seed=0):
    n = len(points)
    if n < 2:
        return 0.0
        
    pts = list(points)
    random.Random(seed).shuffle(pts)
    
    delta = abs(pts[0] - pts[1])
    for i in range(2, n):
        delta = min(delta, abs(pts[i] - pts[i-1]))
        
    if delta == 0:
        return 0.0

    half_delta = delta / 2.0
    buckets = {}
    
    def get_bucket(x):
        return int(x // half_delta)

    for i in range(n):
        p = pts[i]
        b = get_bucket(p)
        found = False
        
        for offset in (-1, 0, 1):
            if (b + offset) in buckets:
                q = buckets[b + offset]
                dist = abs(p - q)
                if dist < delta:
                    delta = dist
                    found = True
                    
        if found:
            if delta == 0:
                return 0.0
            half_delta = delta / 2.0
            buckets.clear()
            for j in range(i + 1):
                buckets[get_bucket(pts[j])] = pts[j]
        else:
            buckets[b] = p
            
    return delta

if __name__ == "__main__":
    random.seed(42)
    pts = [random.uniform(0, 1000) for _ in range(1000)]
    print("Distancia mínima (esperado O(n)):", closest_pair_1d(pts))
    
    pts_sorted = sorted(pts)
    min_dist = min(pts_sorted[i] - pts_sorted[i-1] for i in range(1, len(pts_sorted)))
    print("Distancia mínima (fuerza bruta):  ", min_dist)