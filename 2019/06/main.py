from collections import defaultdict, deque


def build(pairs):
    m = defaultdict(list)
    for pair in pairs:
        a, b = pair.strip().split(")")
        m[a].append(b)
    return m


def orbits(m):
    seen = set()
    alldeps = set()
    for vl in m.values():
        for v in vl:
            alldeps.add(v)
    root = [k for k in m.keys() if k not in alldeps][0]
    q = deque([(root, 0)])
    total = 0
    while q:
        n, ct = q.popleft()
        total += ct
        seen.add(n)
        for c in m[n]:
            if c not in seen:
                q.append((c, ct + 1))
    return total


tdata = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".split()
assert orbits(build(tdata)) == 42


def dist(m):
    rm = {}
    for k, vs in m.items():
        for v in vs:
            rm[v] = k
    paths = []
    for start in ("YOU", "SAN"):
        curr = start
        path = []
        while True:
            path.append(curr)
            if curr not in rm:
                break
            curr = rm[curr]
        paths.append(path)
    a, b = paths
    while a[-1] == b[-1]:
        a.pop()
        b.pop()
    return len(a + b) - 2


tdata2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".split()
assert dist(build(tdata2)) == 4


def main():
    with open("in.txt", "r") as f:
        pairs = f.readlines()
        m = build(pairs)
        # print(orbits(m))
        print(dist(m))


if __name__ == "__main__":
    main()
