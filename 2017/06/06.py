input_str = '11 11 13 7 0 15 5 5 4 4 1 1 7 1 15 11'
arr = [int(n) for n in input_str.split()]
hashes = set()
ct = 0
while tuple(arr) not in hashes:
    hashes.add(tuple(arr))
    m = max(arr)
    maxes = [i for i, j in enumerate(arr) if j == m]
    i = maxes[0]
    arr[i] = 0
    while m > 0:
        i += 1
        if i == len(arr):
            i = 0
        arr[i] += 1
        m -= 1
    ct += 1
print(ct)
