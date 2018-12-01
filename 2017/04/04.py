ct = 0
with open('in.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if len(line.split()) == len(set(line.split())):
            ct += 1

    print(ct)
