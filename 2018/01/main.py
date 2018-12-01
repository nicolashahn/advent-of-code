with open('in.txt', 'r') as f:
    ret = 0
    lines = f.readlines()
    for line in lines:
        ret += int(line)
    print(ret)
