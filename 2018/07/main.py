from collections import defaultdict
from string import ascii_uppercase

def time(k):
    return ascii_uppercase.index(k) + 61
    # for tiny_in.txt example
    # return ascii_uppercase.index(k) + 1

with open('in.txt', 'r') as f:
    lines = f.readlines()
    splitted = [line.split() for line in lines]
    pairs = [(s[1], s[7]) for s in splitted]
    parentmap = defaultdict(list)
    for k,v in pairs:
        parentmap[v].append(k)
        parentmap[k] += []

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

with open('in.txt', 'r') as f:
    lines = f.readlines()
    splitted = [line.split() for line in lines]
    pairs = [(s[1], s[7]) for s in splitted]
    parentmap = defaultdict(list)
    for k, v in pairs:
        parentmap[v].append(k)
        parentmap[k] += []

    times = {k: time(k) for k in parentmap.keys()}
    workers = [k for k, v in parentmap.items() if not v]

    secs = 0
    queue = []
    seen = set(workers)
    while workers:
        seen.update(workers)
        secs += 1
        for w in sorted(workers):
            times[w] -= 1
            if times[w] <= 0:
                queue.append(w)
        for step in queue:
            if step in workers:
                del workers[workers.index(step)]
            for k, klist in parentmap.items():
                if step in klist:
                    del klist[klist.index(step)]
                if not klist and k not in seen and len(workers) < 5:
                    workers.append(k)
    # Part 2
    print(secs)
