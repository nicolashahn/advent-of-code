from collections import defaultdict


def execute(prog, _input):
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
            # input is processed in reverse order
            prog[a] = _input.pop()
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


def execute_collect(prog, _input):
    """ Collects output into a list """
    gen = execute(prog, _input)
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


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# clockwise
CWISE = (UP, RIGHT, DOWN, LEFT)


def p1(prog, s_in):
    _in = [s_in]
    x, y = 0, 0
    # direction index (in CWISE)
    di = 0
    bot = execute(prog[:], _in)
    colors = defaultdict(int)
    # is the output giving a color? (False would mean a direction)
    on_col = True
    for out in bot:
        if on_col:
            colors[(x, y)] = out
        else:
            di = (di + (1 if out == 1 else -1)) % len(CWISE)
            mx, my = CWISE[di]
            x += mx
            y += my
            _in.append(colors[(x, y)])
        on_col = not on_col
    return colors


def p2(colors):
    xs = [x for x, y in colors.keys()]
    ys = [y for x, y in colors.keys()]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    for y in range(miny, maxy + 1):
        row = ""
        for x in range(minx, maxx + 1):
            row += "#" if colors[(x, y)] else " "
        print(row)


def main():
    tests()
    with open("in.txt", "r") as f:
        prog = [int(i) for i in f.readlines()[0].split(",")]
        colors = p1(prog[:], 0)
        assert len(colors) == 1771
        p2(p1(prog[:], 1))


if __name__ == "__main__":
    main()
