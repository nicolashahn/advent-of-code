from collections import Counter

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
    if ti != 1:
        continue
    actual = p1(*parse_input(test))
    if actual == expected:
        print("Test {} passed".format(ti))
    else:
        print("Test {} failed, actual = {} expected = {}".format(ti, actual, expected))


def main():
    with open("in.txt", "r") as f:
        w1, w2 = parse_input(f.read())
        print(p1(w1, w2))


if __name__ == "__main__":
    main()
