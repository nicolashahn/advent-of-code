with open('in.txt', 'r') as f:
    rows = [r.split() for r in f.read().split('\n')]
    s = 0
    for r in rows:
        int_r = [int(n) for n in r]
        _min = float('inf')
        _max = float('-inf')
        for n in int_r:
            _min = min(_min, n)
            _max = max(_max, n)
        s += _max - _min
    print(s)
