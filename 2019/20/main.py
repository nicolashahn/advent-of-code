from collections import defaultdict, deque

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def parse(raw):
    rows = raw.split("\n")
    # portals to coordinates, values are lists of coords up to len 2 (AA and ZZ have 1)
    p2c = defaultdict(list)

    def get_portal(x, y):
        portal = None
        if rows[y][x - 1] in ALPHA:
            portal = rows[y][x - 2] + rows[y][x - 1]
        elif rows[y][x + 1] in ALPHA:
            portal = rows[y][x + 1] + rows[y][x + 2]
        elif rows[y - 1][x] in ALPHA:
            portal = rows[y - 2][x] + rows[y - 1][x]
        elif rows[y + 1][x] in ALPHA:
            portal = rows[y + 1][x] + rows[y + 2][x]
        return portal

    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell == ".":
                portal = get_portal(x, y)
                if portal:
                    p2c[portal].append((x, y))
    return rows, p2c


def p1(grid, p2c):
    sxy = p2c["AA"][0]
    exy = p2c["ZZ"][0]
    # portals represented as mapping of coordinate to coordinate
    c2c = {}
    for _, xys in p2c.items():
        if len(xys) > 1:
            xy1, xy2 = xys
            c2c[xy1] = xy2
            c2c[xy2] = xy1

    q = deque([(sxy, 0)])
    seen = set()
    while q:
        (x, y), d = q.popleft()
        if (x, y) == exy:
            return d
        seen.add((x, y))
        nxys = [
            (nx, ny)
            for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if grid[ny][nx] == "."
        ]
        if (x, y) in c2c:
            nxys.append(c2c[x, y])
        for nxy in nxys:
            if nxy not in seen:
                q.append((nxy, d + 1))
    return float("inf")


def is_outer(grid, x, y):
    return y in (2, len(grid) - 3) or x in (2, len(grid[0]) - 3)


def split_portals(grid, p2c):
    inner, outer = {}, {}
    for p, xys in p2c.items():
        for (x, y) in xys:
            if is_outer(grid, x, y):
                outer[p] = (x, y)
            else:

                inner[p] = (x, y)
    assert len(outer) == (len(inner) + 2)  # AA and ZZ always outer
    return inner, outer


def p2(grid, p2c):
    sxy = p2c["AA"][0]
    exy = p2c["ZZ"][0]
    # portals represented as mapping of coordinate to coordinate
    c2c = {}
    for _, xys in p2c.items():
        if len(xys) > 1:
            xy1, xy2 = xys
            c2c[xy1] = xy2
            c2c[xy2] = xy1

    q = deque([((sxy, 0), 0)])
    seen = set()
    while q:
        ((x, y), lv), d = q.popleft()
        if (x, y) == exy and lv == 0:
            return d
        seen.add(((x, y), lv))
        nxylvs = [
            ((nx, ny), lv)
            for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if grid[ny][nx] == "."
        ]
        if (x, y) in c2c:
            nlv = (lv - 1) if is_outer(grid, x, y) else (lv + 1)
            if nlv >= 0:
                nxylvs.append((c2c[x, y], nlv))
        for nxylv in nxylvs:
            if nxylv not in seen:
                q.append((nxylv, d + 1))
    return float("inf")


def tests():
    pass
    in1 = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """
    in2 = """                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """
    assert p1(*parse(in1)) == 23
    assert p1(*parse(in2)) == 58


def main():
    tests()
    with open("in.txt", "r") as f:
        raw = f.read().strip("\n")
        grid, p2c = parse(raw)
        assert p1(grid, p2c) == 482
        print(p2(grid, p2c))


if __name__ == "__main__":
    main()
