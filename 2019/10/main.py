class Ratio:
    def __init__(self, rad, div):
        rneg, dneg = rad < 0, div < 0
        rad, div = abs(rad), abs(div)
        if rad == 0:
            div = 1
        if div == 0:
            rad = 1
        gcf = 1
        for i in range(2, min(rad, div) + 1):
            gcf = i if (rad % i == 0 and div % i == 0) else gcf
        self.rad = rad // gcf * (-1 if rneg else 1)
        self.div = div // gcf * (-1 if dneg else 1)

    @property
    def pair(self):
        return self.rad, self.div


assert Ratio(10, 5).pair == (2, 1)
assert Ratio(6, 9).pair == (2, 3)
assert Ratio(7, 9).pair == (7, 9)
assert Ratio(-7, 9).pair == (-7, 9)
assert Ratio(7, -9).pair != (-7, 9)


def count(space, sx, sy):
    asteroids = []
    for y, row in enumerate(space):
        for x, c in enumerate(row):
            if c == "#" and ((x, y) != (sx, sy)):
                asteroids.append((x, y))
    blocked = set()
    ct = 0
    s_asteroids = sorted(asteroids, key=lambda a: abs(sx - a[0]) + abs(sy - a[1]))
    for ax, ay in s_asteroids:
        if (ax, ay) in blocked:
            continue
        # d for distance
        dx, dy = Ratio(ax - sx, ay - sy).pair
        # b for blocked
        bx, by = ax, ay
        while 0 <= bx < len(space[0]) and 0 <= by < len(space):
            bx += dx
            by += dy
            blocked.add((bx, by))
        ct += 1
    return ct


def p1(space):
    best = 0
    for y, row in enumerate(space):
        for x, c in enumerate(row):
            if c == "#":
                ct = count(space, x, y)
                best = max(best, ct)
    return best


test = [
    l.strip()
    for l in """.#..#
.....
#####
....#
...##""".split()
]

assert p1(test) == 8


def main():
    with open("in.txt", "r") as f:
        space = [l.strip() for l in f.readlines()]
        print(p1(space))


if __name__ == "__main__":
    main()
