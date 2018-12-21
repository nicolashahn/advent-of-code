import re
import sys

sys.setrecursionlimit(9001)


def display(grid, water):
    out = []
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            if (x, y) in water:
                if water[(x,y)]:
                    row.append('v')
                else:
                    row.append('o')
            else:
                row.append(grid[y][x])
        out.append(''.join(row))
    print('\n'.join(out) + '\n')


def valid(grid, x, y):
    if (
            0 <= x < len(grid[0]) and
            0 <= y < len(grid)
    ):
        return grid[y][x] != '#'
    return False


def get_neighbors(grid, src_xy):
    x, y = src_xy
    if valid(grid, x, y + 1):
        return [(x, y + 1)]
    return [(nx, ny) for nx, ny in [
        (x + 1, y),
        (x - 1, y),
    ] if valid(grid, nx, ny)]


def drip(grid, xy):
    water = {}

    def inner(grid, xy, water):
        # display(grid, water)
        x, y = xy
        if y == len(grid):
            # means we hit the bottom
            return True
        if not valid(grid, *xy):
            return False
        if xy not in water:
            water[xy] = water.get((x, y + 1), False)
            if water[xy]:
                return True
            if inner(grid, (x, y + 1), water):
                water[xy] = True
                return True
            left = inner(grid, (x + 1, y), water)
            if left:
                lx = x
                while (lx, y) in water:
                    water[(lx, y)] = True
                    lx -= 1
            right = inner(grid, (x - 1, y), water)
            if right:
                lx = x
                while (lx, y) in water:
                    water[(lx, y)] = True
                    lx += 1
            water[xy] = left or right  # or (x, y + 1) in water
            return water[xy]
        return water[xy]

    inner(grid, xy, water)
    del water[xy]
    return water


def p1(lines):
    clay_xys = []
    for line in lines:
        a, b, c = [int(i) for i in re.findall('\d+', line)]
        for i in range(b, c + 1):
            if line.startswith('x'):
                xy = (a, i)
            else:
                xy = (i, a)
            clay_xys.append(xy)
    minx = min([x for x, y in clay_xys])
    maxx = max([x for x, y in clay_xys])
    maxy = max([y for x, y in clay_xys])
    miny = min([y for x, y in clay_xys])
    grid = [['.' for _ in range(minx, maxx + 3)]
            for _ in range(miny - 5, maxy + 1)]
    XOFFSET = minx - 1
    for x, y in clay_xys:
        grid[y][x - XOFFSET] = '#'
    grid[0][500 - XOFFSET] = '+'
    water = drip(grid, (500 - XOFFSET, miny - 1))
    display(grid, water)
    # print(water)
    print(len(water))
    # Part 2
    print(len([v for v in water.values() if not v]))


with open('in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
