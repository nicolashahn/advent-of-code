from collections import Counter, defaultdict

DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


# for debugging
def print_d(d):
    xs = [x for x, y in d.keys()]
    ys = [y for x, y in d.keys()]
    print(min(xs), min(ys), max(xs), max(ys))
    for y in range(min(ys) - 5, max(ys) + 1 + 5):
        line = ""
        for x in range(min(xs) - 5, max(xs) + 1 + 5):
            line += str(d[(x, y)])
        print(line.replace("0", "."))


def p1(w1, w2):
    d = Counter()
    for wi, w in ((1, w1), (2, w2)):
        cx, cy = 0, 0
        for corner in w:
            dir = corner[0]
            dist = int(corner[1:])
            for i in range(dist):
                cx += DIRS[dir][0]
                cy += DIRS[dir][1]
                d[(cx, cy)] |= wi
    intersections = [k for k, v in d.items() if v == 3]
    return min([abs(x) + abs(y) for x, y in intersections])


def parse_input(raw):
    return [w.split(",") for w in raw.split()]


tests = [
    (
        """R8,U5,L5,D3
U7,R6,D4,L4""",
        6,
    ),
    (
        """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""",
        159,
    ),
    (
        """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7""",
        135,
    ),
]
for ti, (test, expected) in enumerate(tests):
    actual = p1(*parse_input(test))
    if actual == expected:
        print("Test for p1 {} passed".format(ti))
    else:
        print(
            "Test for p1 {} failed, actual = {} expected = {}".format(
                ti, actual, expected
            )
        )


def p2(w1, w2):
    d1 = Counter()
    d2 = Counter()
    for d, w in ((d1, w1), (d2, w2)):
        cx, cy = 0, 0
        tdist = 0
        for corner in w:
            dir = corner[0]
            dist = int(corner[1:])
            for i in range(dist):
                tdist += 1
                cx += DIRS[dir][0]
                cy += DIRS[dir][1]
                d[(cx, cy)] = tdist
    ans = float("inf")
    for xy in d1:
        if xy in d2:
            ans = min(ans, d1[xy] + d2[xy])
    return ans


tests2 = [
    (
        """R8,U5,L5,D3
U7,R6,D4,L4""",
        30,
    ),
    (
        """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""",
        610,
    ),
    (
        """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7""",
        410,
    ),
]
for ti, (test, expected) in enumerate(tests2):
    actual = p2(*parse_input(test))
    if actual == expected:
        print("Test for p2 {} passed".format(ti))
    else:
        print(
            "Test for p2 {} failed, actual = {} expected = {}".format(
                ti, actual, expected
            )
        )


def main():
    with open("in.txt", "r") as f:
        w1, w2 = parse_input(f.read())
        # print(p1(w1, w2))
        print(p2(w1, w2))


if __name__ == "__main__":
    main()
