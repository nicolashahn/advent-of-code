with open('in.txt', 'r') as f:
    arr = [int(n) for n in f.readlines()]
    i = 0
    ct = 0
    while i < len(arr):
        next_i = i + arr[i]
        arr[i] += 1
        ct += 1
        i = next_i
    print(ct)
