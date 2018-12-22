# input:
depth = 11541
target = 14, 778

# example input:
# depth = 510
# target = 10, 10

# memoization for erosion
mem = {}


# mapping from type value to display character
type_display_map = {
    0: '.',
    1: '=',
    2: '|',
}


def display():
    tx, ty = target
    out = []
    for y in range(ty + 1):
        for x in range(tx + 1):
            out.append(type_display_map[mem[(x, y)] % 3])
        out.append('\n')
    print(''.join(out))


def get_erosion(x, y):
    if (x, y) not in mem:
        gi = None
        if (x, y) == (0, 0) or (x, y) == target:
            gi = 0
        elif x == 0:
            gi = 48271 * y
        elif y == 0:
            gi = 16807 * x
        else:
            gi = get_erosion(x, y - 1) * get_erosion(x - 1, y)
        erosion = (gi + depth) % 20183
        mem[(x, y)] = erosion
    return mem[(x, y)]


def p1():
    tx, ty = target
    res = 0
    for x in range(tx + 1):
        for y in range(ty + 1):
            erosion = get_erosion(x, y)
            res += erosion % 3
    display()
    return res


print(p1())
