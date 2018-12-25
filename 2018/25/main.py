

def close(p, q):
    return (
        abs(p[0] - q[0]) +
        abs(p[1] - q[1]) +
        abs(p[2] - q[2]) +
        abs(p[3] - q[3])
    ) <= 3


def p1(lines):
    points = [tuple([int(i) for i in l.split(',')]) for l in lines]
    unions = []
    for i, p in enumerate(points):
        for j, q in enumerate(points[:i]):
            if close(p, q):
                unions.append((i, j))
    idxs = list(range(len(points)))
    for ip, iq in unions:
        ip, iq = sorted([ip, iq])
        for ik, k in enumerate(idxs):
            if k in (idxs[ip], idxs[iq]):
                idxs[ik] = idxs[ip]
    print(len(set(idxs)))



with open('in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
