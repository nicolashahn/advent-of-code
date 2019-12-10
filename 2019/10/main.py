def parse_in(raw):
    return [list(l.strip()) for l in raw.split()]


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


def get_vis(space, sx, sy):
    asts = []
    for y, row in enumerate(space):
        for x, c in enumerate(row):
            if c == "#" and ((x, y) != (sx, sy)):
                asts.append((x, y))
    blocked = set()
    visible = set()
    # sorted by dist to sx,sy
    sort_asts = sorted(asts, key=lambda a: abs(sx - a[0]) + abs(sy - a[1]))
    for ax, ay in sort_asts:
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
        visible.add((ax, ay))
    return visible


def p1(space):
    best = 0
    bxy = None
    for y, row in enumerate(space):
        for x, c in enumerate(row):
            if c == "#":
                ct = len(get_vis(space, x, y))
                if best < ct:
                    best = ct
                    bxy = x, y
    return best, bxy


test_space = parse_in(
    """.#..#
.....
#####
....#
...##"""
)


assert p1(test_space)[0] == 8


def laser(space, sx, sy, vis):
    # the asteroids that were destroyed in this rotation in order
    batch = []
    # relative position compared to base (sx,sy)
    rpos = [(x - sx, y - sy) for x, y in vis]
    # upper-right quadrant, processed 1st
    urq = [(x, y) for x, y in rpos if y < 0 and x >= 0]
    # lower-right, processed 2nd
    lrq = [(x, y) for x, y in rpos if y >= 0 and x > 0]
    # lower-left, processed 3rd
    llq = [(x, y) for x, y in rpos if y > 0 and x <= 0]
    # upper-left, processed 4th
    ulq = [(x, y) for x, y in rpos if y <= 0 and x < 0]
    assert len(urq + lrq + llq + ulq) == len(vis)

    def comp(xy):
        x, y = xy
        if x == 0:
            return float("inf")
        return float(abs(y)) / float(abs(x))

    # put all quadrants in sorted order if rotating clockwise
    surq = sorted(urq, key=comp, reverse=True)
    slrq = sorted(lrq, key=comp)
    sllq = sorted(llq, key=comp, reverse=True)
    sulq = sorted(ulq, key=comp)
    # start blasting
    for quad in (surq, slrq, sllq, sulq):
        for x, y in quad:
            # convert relative back to absolute pos
            ax, ay = sx + x, sy + y
            batch.append((ax, ay))
            space[ay][ax] = "."
    return batch


def p2(space, x, y):
    # list of destroyed asteroids in order of destruction
    ds = []
    # this list comp flattens space to a 1d list
    while "#" in [p for row in space for p in row]:
        vis = get_vis(space, x, y)
        batch = laser(space, x, y, vis)  # mutates space
        if not batch:
            break
        ds += batch
        if len(ds) >= 200:
            ax, ay = ds[199]
            return ax * 100 + ay
    print("p2 broken")


test_space2 = parse_in(
    """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
)

assert p2(test_space2, 11, 13) == 802


def main():
    with open("in.txt", "r") as f:
        space = parse_in(f.read())
        p1_ans, xy = p1(space)
        assert p1_ans == 319
        assert p2(space, *xy) == 517


if __name__ == "__main__":
    main()
