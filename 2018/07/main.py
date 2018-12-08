from collections import defaultdict

with open('in.txt', 'r') as f:
    lines = f.readlines()
    splitted = [line.split() for line in lines]
    pairs = [(s[1], s[7]) for s in splitted]
    childmap = defaultdict(list)
    parentmap = defaultdict(list)
    for k,v in pairs:
        childmap[k].append(v)
        parentmap[v].append(k)
        childmap[v] += []
        parentmap[k] += []
    print(childmap)
    print(parentmap)

    queue = [k for k, v in parentmap.items() if not v]

    order = []
    while queue:
        curr, queue = queue[0], queue[1:]
        order.append(curr)
        for k, klist in parentmap.items():
            if curr in klist:
                del klist[klist.index(curr)]
                if not klist:
                    queue.append(k)
        queue.sort()
    # Part 1
    print(''.join(order))
