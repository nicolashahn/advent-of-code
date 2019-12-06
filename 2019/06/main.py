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
        print(n, ct)
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


def main():
    with open("in.txt", "r") as f:
        pairs = f.readlines()
        m = build(pairs)
        print(orbits(m))


if __name__ == "__main__":
    main()
