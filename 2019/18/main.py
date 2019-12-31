from collections import deque
from itertools import combinations
from heapq import heapify, heappush, heappop
from functools import lru_cache

ALPHA = "abcdefghijklmnopqrtstuvwxyz"


def parse(raw):
    grid = {}
    keys = {}
    doors = {}
    starts = []
    rawlines = raw.split("\n")
    for y, line in enumerate(rawlines):
        for x, c in enumerate(line):
            grid[x, y] = c
            if c in ALPHA:
                keys[c] = (x, y)
            elif c in ALPHA.upper():
                doors[c] = (x, y)
            elif c == "@":
                grid[x, y] = "."
                starts.append((x, y))
    return grid, starts, keys, doors


def printgrid(grid, sxys=None):
    if not sxys:
        sxys = []
    maxx = max([x for x, y in grid])
    maxy = max([y for x, y in grid])
    for y in range(maxy + 1):
        row = ""
        for x in range(maxx + 1):
            row += "@" if (x, y) in sxys else grid[x, y]
        print(row)


def getdist(grid, door_xys, sxy, exy):
    """ Get the min path len between two points in the maze and the doors on path """
    q = deque([(sxy, set(), 0)])
    seen = set()
    while q:
        (x, y), doors, d = q.popleft()
        if (x, y) == exy:
            return d, doors
        seen.add((x, y))
        if grid[x, y] in ALPHA.upper():
            doors.add(grid[x, y])
        for nxy in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if grid[nxy] != "#" and nxy not in seen:
                q.append((nxy, doors.copy(), d + 1))
    return float("inf"), set()


def getallkeydists(grid, key_xys, door_xys):
    """ Compute getdist() for every pair of keys and store results """
    kdists = {}
    for k1, k2 in combinations(key_xys, 2):
        kxy1 = key_xys[k1]
        kxy2 = key_xys[k2]
        kdists[frozenset([k1, k2])] = getdist(grid, door_xys, kxy1, kxy2)
    return kdists


# NOTE this doesn't make a lot of sense because it's halfway converted to allow for
# multiple robot positions. I gave up on that and started fresh in p2().  Didn't change
# it back because it works as-is and this is not code I plan on maintaining.
def p1(grid, sxys, key_xys, door_xys):
    """ Given a starting point, find the len of the shortest path to find all keys """
    allkeys = set(key_xys.keys())
    kdists = getallkeydists(grid, key_xys, door_xys)
    sdists = {
        k: getdist(grid, door_xys, sxy, kxy)
        for k, kxy in key_xys.items()
        for sxy in sxys
    }
    q = [(d, k) for k, (d, reqds) in sdists.items() if not reqds]

    @lru_cache(None)
    def recfind(k, held):
        held = held | {k}
        if len(held) == len(key_xys):
            return 0
        best = float("inf")
        for nk in allkeys - held:
            dist, doors = kdists[frozenset((k, nk))]
            if all([door.lower() in held for door in doors]):
                best = min(best, dist + recfind(nk, held))
        return best

    best = float("inf")
    for d, k in q:
        best = min(best, d + recfind(k, frozenset()))
    return best


def p2(grid, sxys, key_xys, door_xys):
    """ Same as p1, but with multiple robot positions per state """
    allkeys = set(key_xys.keys())
    for i, sxy in enumerate(sxys):
        key_xys["@{}".format(i)] = sxy
    kdists = getallkeydists(grid, key_xys, door_xys)

    start_ks = tuple("@{}".format(i) for i in range(len(sxys)))
    held = frozenset()

    @lru_cache(None)
    def recfind(ks, held):
        for k in ks:
            if k in ALPHA:
                held = held | {k}
        if len(held) == len(allkeys):
            return 0
        best = float("inf")
        for nk in allkeys - held:
            for i, k in enumerate(ks):
                dist, doors = kdists[frozenset((k, nk))]
                if dist < float("inf") and all(
                    [door.lower() in held for door in doors]
                ):
                    newks = list(ks)
                    newks[i] = nk
                    best = min(best, recfind(tuple(newks), held) + dist)
        return best

    return recfind(start_ks, held)


def updategridp2(grid):
    ngrid = grid.copy()
    cx, cy = 40, 40
    ngrid[cx - 1, cy - 1] = "@"
    ngrid[cx - 1, cy] = "#"
    ngrid[cx - 1, cy + 1] = "@"
    ngrid[cx, cy - 1] = "#"
    ngrid[cx, cy] = "#"
    ngrid[cx, cy + 1] = "#"
    ngrid[cx + 1, cy - 1] = "@"
    ngrid[cx + 1, cy] = "#"
    ngrid[cx + 1, cy + 1] = "@"
    return (
        ngrid,
        [(cx - 1, cy - 1), (cx + 1, cy - 1), (cx - 1, cy + 1), (cx + 1, cy + 1)],
    )


def tests():
    in1 = """
#########
#@....a.#
#########""".strip()
    grid, sxy, key_xys, door_xys = parse(in1)
    in2 = """
#########
#b.A.@.a#
#########""".strip()
    in3 = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""".strip()
    in4 = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""".strip()
    in5 = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""".strip()
    assert p1(*parse(in1)) == 5
    assert p1(*parse(in2)) == 8
    assert p1(*parse(in3)) == 86
    assert p1(*parse(in4)) == 132
    assert p1(*parse(in5)) == 136

    print("tests passed")


def main():
    tests()
    with open("in.txt", "r") as f:
        raw = f.read().strip()
        grid, sxys, key_xys, door_xys = parse(raw)
        assert p1(grid, sxys, key_xys, door_xys) == 7430
        p2grid, p2sxys = updategridp2(grid)
        assert p2(p2grid, p2sxys, key_xys, door_xys) == 1864


if __name__ == "__main__":
    main()
