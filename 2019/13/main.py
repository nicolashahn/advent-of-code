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
            prog[a] = next(in_gen)
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


def p1(prog):
    out = execute_collect(prog, [])
    grid = {}
    for i in range(0, len(out), 3):
        x, y, t = out[i : i + 3]
        grid[x, y] = t
    return len([t for t in grid.values() if t == 2])


TILES = {0: " ", 1: "|", 2: "#", 3: "-", 4: "o"}


def printgrid(grid, scores=[0]):
    score = grid.get((-1, 0), 0)
    if score != scores[-1]:
        scores.append(score)
    print("score history: {}".format(scores))
    xs = [x for x, y in grid]
    ys = [y for x, y in grid]
    maxx, maxy = max(xs), max(ys)
    for y in range(0, maxy + 1):
        row = ""
        for x in range(0, maxx + 1):
            row += TILES[grid[x, y]] if (x, y) in grid else " "
        print(row)


PADDLE = 3
BALL = 4


def gen_input(state):
    # previous ball x position
    pbx, _ = state.get(BALL)
    while True:
        # current paddle position
        cx, cy = state.get(PADDLE)
        # current ball position
        bx, by = state.get(BALL)
        # future ball x position
        fbx = bx + (bx - pbx)
        # if about to bounce, predict direction after bounce
        if cy == by + 1:
            if cx < bx:
                yield 1
            elif cx > bx:
                yield -1
            else:
                yield 0
        # else, chase the ball
        elif cx > fbx:
            yield -1
        elif cx < fbx:
            yield 1
        else:
            yield 0
        pbx = bx


def p2(prog):
    prog[0] = 2
    _in = []
    state = {}
    buf = []
    _in = gen_input(state)
    for out in execute(prog, _in):
        buf.append(out)
        if len(buf) == 3:
            x, y, t = buf
            if t in (3, 4):
                state[t] = x, y
            elif x == -1:
                state[-1] = t
            buf = []
    return state[-1]


def main():
    tests()
    with open("in.txt", "r") as f:
        prog = [int(i) for i in f.readlines()[0].split(",")]
        print(p2(prog[:]))


if __name__ == "__main__":
    main()
