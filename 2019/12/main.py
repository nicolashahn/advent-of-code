def vadd(v1, v2):
    assert len(v1) == len(v2)
    return [x + y for x, y in zip(v1, v2)]


def grav_v(v1, v2):
    nv = []
    for x, y in zip(v1, v2):
        if x == y:
            nv.append(0)
        elif x < y:
            nv.append(1)
        else:
            nv.append(-1)
    return nv


def sim(pos, vel):
    for i in range(len(pos)):
        pi = pos[i]
        for j in range(len(pos)):
            if j != i:
                pj = pos[j]
                vel[i] = vadd(vel[i], grav_v(pi, pj))
    for i in range(len(pos)):
        pos[i] = vadd(vel[i], pos[i])


def tot_en(pos, vel):
    tot = 0
    for i in range(len(pos)):
        pot = sum([abs(p) for p in pos[i]])
        kin = sum([abs(p) for p in vel[i]])
        tot += pot * kin
    return tot


def p1(pos, steps):
    vel = [[0, 0, 0] for _ in pos]
    for i in range(steps):
        sim(pos, vel)
    return tot_en(pos, vel)


def parse_in(raw):
    return [
        [int(i) for i in line.split(",")]
        for line in [
            "".join([c for c in line if c in "-,1234567890"])
            for line in raw.split("\n")
        ]
    ]


test = parse_in(
    """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
)
assert p1(test[:], 10) == 179


def lcm(ns):
    i = 2
    while i < max(ns):
        if all([n % i == 0 for n in ns]):
            ns = [n // i for n in ns]
        else:
            i += 1
    ans = 1
    for n in ns:
        ans *= n
    return ans


assert lcm([18, 28, 44]) == 2772


def p2(pos):
    vel = [[0, 0, 0] for _ in pos]
    inits = [[p[i] for p in pos] + [v[i] for v in vel] for i in range(3)]
    pers = [None, None, None]
    i = 0
    while True:
        sim(pos, vel)
        i += 1
        for j in range(3):
            xs = [p[j] for p in pos] + [v[j] for v in vel]
            if xs == inits[j] and pers[j] is None:
                pers[j] = i
        if all(pers):
            return lcm(pers)


assert p2(test[:]) == 2772


def main():
    raw = """<x=-6, y=-5, z=-8>
<x=0, y=-3, z=-13>
<x=-15, y=10, z=-11>
<x=-3, y=-8, z=3>"""
    pos = parse_in(raw)
    # print(p1(pos[:], 1000))
    print(p2(pos[:]))


if __name__ == "__main__":
    main()
