from collections import deque


def execute(prog, in_gen):
    """ Generator, yields output """

    def read_op(op):
        op = str(op).zfill(5)
        modes = [op[i] for i in range(3)][::-1]
        opcode = int(op[-2:])
        return opcode, modes

    # instruction pointer
    i = 0
    # relative base
    rb = 0
    # do not increment instruction pointer if true (for ops 5,6)
    jumped = False
    # for debugging
    history = []
    # number of registers each op uses
    oplens = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 0}
    # add extra memory
    prog += [0] * 2 ** 16

    while i < len(prog):
        history.append(i)
        opcode, modes = read_op(prog[i])

        def mmap(m, j):  # map of {mode: address to use as param}
            return {"0": prog[j], "1": j, "2": prog[j] + rb}.get(m)

        oplen = oplens[opcode]
        # a, b, c are addresses of op's params after accounting for mode
        if oplen >= 2:
            a = mmap(modes[0], i + 1)
        if oplen >= 3:
            b = mmap(modes[1], i + 2)
        if oplen >= 4:
            c = mmap(modes[2], i + 3)

        # execute op
        if opcode == 1:
            prog[c] = prog[a] + prog[b]
        elif opcode == 2:
            prog[c] = prog[a] * prog[b]
        elif opcode == 3:
            try:
                prog[a] = next(in_gen)
            except StopIteration:
                print("Stopping execution, received no input")
                break
        elif opcode == 4:
            yield prog[a]
        elif opcode == 5:
            if prog[a] != 0:
                i = prog[b]
                jumped = True
        elif opcode == 6:
            if prog[a] == 0:
                i = prog[b]
                jumped = True
        elif opcode == 7:
            prog[c] = 1 if prog[a] < prog[b] else 0
        elif opcode == 8:
            prog[c] = 1 if prog[a] == prog[b] else 0
        elif opcode == 9:
            rb += prog[a]
        elif opcode == 99:
            break
        else:
            print(
                "execute() is broken, history of instruction positions: {}".format(
                    history
                )
            )
            __import__("pdb").set_trace()
        if not jumped:
            i += oplen
        else:
            jumped = False


def execute_collect(prog, in_list):
    """ Collects output into a list """
    gen = execute(prog, iter(in_list))
    out = []
    for output in gen:
        out.append(output)
    return out


def tests():
    # check equality w/position mode (opcode 8)
    assert execute_collect([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8]) == [1]
    assert execute_collect([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [7]) == [0]
    # check less than w/position mode (opcode 7)
    assert execute_collect([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7]) == [1]
    assert execute_collect([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8]) == [0]
    # check equality w/immediate mode (opcode 8)
    assert execute_collect([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8]) == [1]
    assert execute_collect([3, 3, 1108, -1, 8, 3, 4, 3, 99], [7]) == [0]
    # check less than w/position mode (opcode 7)
    assert execute_collect([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7]) == [1]
    assert execute_collect([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8]) == [0]
    # jump tests
    assert execute_collect(
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0]
    ) == [0]
    assert execute_collect(
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [5]
    ) == [1]
    assert execute_collect([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]) == [
        0
    ]
    assert execute_collect([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [1]) == [
        1
    ]
    # longer example from problem description
    long_prog = eval(
        """[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]"""
    )
    assert execute_collect(long_prog[:], [7]) == [999]
    assert execute_collect(long_prog[:], [8]) == [1000]
    assert execute_collect(long_prog[:], [9]) == [1001]
    quine = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert execute_collect(quine[:], []) == quine[:]
    assert execute_collect([1102, 34915192, 34915192, 7, 4, 7, 99, 0], []) == [
        34915192 ** 2
    ]
    assert execute_collect([104, 1125899906842624, 99], []) == [1125899906842624]
    print("tests passed")


UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

DIRS = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)}
OPP_DIRS = {v: k for k, v in DIRS.items()}
TILES = {0: "|", 1: " ", 2: "*"}


def printgrid(grid, cx, cy):
    xs = [x for x, y in grid]
    ys = [y for x, y in grid]
    maxx, maxy = max(xs), max(ys)
    minx, miny = min(xs), min(ys)
    for y in range(miny, maxy + 1):
        row = ""
        for x in range(minx, maxx + 1):
            if cx == x and cy == y:
                row += "D"
            else:
                row += TILES[grid[x, y]] if (x, y) in grid else " "
        print(row)


def explore(out, grid):
    cx, cy = 0, 0
    seen = {(0, 0)}
    stack = [(0, 0)]
    while True:
        adjs = [
            (d, (cx + dx, cy + dy))
            for d, (dx, dy) in DIRS.items()
            if (cx + dx, cy + dy) not in seen
        ]
        if adjs:
            mv, (nx, ny) = adjs[0]
            stack.append((nx, ny))
            seen.add((nx, ny))
        else:
            stack.pop()
            if not stack:
                break
            px, py = stack[-1]
            mv = OPP_DIRS[px - cx, py - cy]
        yield mv
        dx, dy = DIRS[mv]
        if out[-1] == 0:
            grid[cx + dx, cy + dy] = 0
            stack.pop()
        else:
            if out[-1] == 2:
                print("FOUND: {} {}".format(cx, cy))
            cx += dx
            cy += dy
            grid[cx, cy] = out[-1]


def bfs1(grid):
    # x,y,dist from 0,0
    q = deque([(0, 0, 0)])
    while q:
        x, y, d = q.popleft()
        if grid[x, y] == 2:
            return d
        if grid.get((x, y)) != 0:
            grid[x, y] = 0
        for nx, ny in [
            (x + dx, y + dy) for dx, dy in DIRS.values() if grid.get((x + dx, y + dy))
        ]:
            q.append((nx, ny, d + 1))


def bfs2(grid):
    # starting dist = 1 here because takes 1 min to fill first tile w/oxygen
    q = deque([(0, 0, 1)])
    seen = set()
    maxd = 0
    while q:
        x, y, d = q.popleft()
        maxd = max(maxd, d)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        for nx, ny in [
            (x + dx, y + dy) for dx, dy in DIRS.values() if grid.get((x + dx, y + dy))
        ]:
            q.append((nx, ny, d + 1))
    return maxd


def run_explore(prog):
    out = []
    grid = {(0, 0): 1}
    _in = explore(out, grid)
    for resp in execute(prog, _in):
        out.append(resp)
    return grid


def p1(prog):
    return bfs1(run_explore(prog))


def p2(prog):
    return bfs2(run_explore(prog))


def main():
    tests()
    with open("in.txt", "r") as f:
        prog = [int(i) for i in f.readlines()[0].split(",")]
        assert p1(prog[:]) == 404
        assert p2(prog[:]) == 406


if __name__ == "__main__":
    main()
