def find_candidates_nk(arr, k):
    counts = {}
    
    for x in arr:
        if x in counts:
            counts[x] += 1
        elif len(counts) < k - 1:
            counts[x] = 1
        else:
            to_remove = []
            for key in counts:
                counts[key] -= 1
                if counts[key] == 0:
                    to_remove.append(key)
            for key in to_remove:
                del counts[key]
                
    return list(counts.keys())


def find_candidates_n3(arr):
    return find_candidates_nk(arr, 3)


def correct_majority_n3(arr):
    candidates = find_candidates_n3(arr)
    res = []
    for c in candidates:
        if arr.count(c) > len(arr) / 3:
            res.append(c)
    return res


def buggy_majority_n3(arr):
    return find_candidates_n3(arr)


def test_generator_binary():
    import random
    caught = False
    for _ in range(1000):
        n = random.randint(1, 100)
        arr = [random.choice(['A', 'B']) for _ in range(n)]
        if set(buggy_majority_n3(arr)) != set(correct_majority_n3(arr)):
            caught = True
            break
    if caught:
        print("Binary generator: Caught the bug.")
    else:
        print("Binary generator: Failed to catch the bug.")


def test_generator_flawed():
    import random
    caught = False
    for _ in range(1000):
        k = random.randint(1, 30)
        arr = ['A', 'B', 'C'] * k
        random.shuffle(arr)
        if set(buggy_majority_n3(arr)) != set(correct_majority_n3(arr)):
            caught = True
            break
    if caught:
        print("Flawed generator: Caught the bug.")
    else:
        print("Flawed generator: Did not catch the bug (as expected).")


if __name__ == "__main__":
    test_generator_binary()
    test_generator_flawed()