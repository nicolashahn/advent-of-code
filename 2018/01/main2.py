with open('in.txt', 'r') as f:
    ret = 0
    seen = set()
    lines = [int(l) for l in f.readlines()]
    while True:
        for line in lines:
            ret += line
            if ret in seen:
                print(ret)
                exit()
            seen.add(ret)
