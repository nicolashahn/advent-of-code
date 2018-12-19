import re


XOFFSET = None


def display(grid, water):
    out = []
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            ox, oy = (x + XOFFSET, y + 1)
            if (ox, oy) in water:
                row.append('~')
            else:
                row.append(grid[y][x])
        out.append(''.join(row))
    print('\n'.join(out))


def valid(grid, x, y):
    ox, oy = (x - XOFFSET, y - 1)
    if (
            0 <= ox < len(grid[0]) and
            0 <= oy < len(grid)
    ):
        return grid[ox][oy] != '#'
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
    water = set()

    def inner(grid, xy, water):
        x, y = xy
        if y == len(grid):
            # means we hit the bottom
            return True
        if y < len(grid) and xy not in water:
            water.add(xy)
            if valid(grid, x, y+1):
                if inner(grid, (x, y+1), water):
                    return True
            # l_bot = False
            # if valid(grid, x-1, y):
                # if inner(grid, (x-1, y), water):
                    # l_bot = True
            # if valid(grid, x+1, y):
                # if inner(grid, (x+1, y), water):
                    # if l_bot: return True
    inner(grid, xy, water)
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
    grid = [['.' for _ in range(minx, maxx + 3)]
            for _ in range(maxy + 1)]
    global XOFFSET
    XOFFSET = minx - 1
    for x, y in clay_xys:
        grid[y][x - XOFFSET] = '#'
    grid[0][500 - XOFFSET] = '+'
    water = drip(grid, (500, 0))
    print(water)
    display(grid, water)



with open('tiny_in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
