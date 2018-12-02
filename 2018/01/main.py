# Part 1
with open('in.txt', 'r') as f:
    ret = 0
    lines = f.readlines()
    for line in lines:
        ret += int(line)
    print(ret)


# Part 2
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
