from collections import Counter


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


def printgrid(grid, inters=None):
    if not inters:
        inters = []
    maxx = max([x for x, y in grid])
    maxy = max([y for x, y in grid])
    for y in range(maxy + 1):
        row = ""
        for x in range(maxx + 1):
            row += grid[x, y] if (x, y) not in inters else "O"
        print(row)


def togrid(out):
    grid = {}
    x = 0
    y = 0
    for i in out:
        if i == 10:
            x = 0
            y += 1
        else:
            grid[x, y] = chr(i)
            x += 1
    return grid


def p1(prog):
    out = execute_collect(prog, [])
    grid = togrid(out)
    inters = []
    for x, y in grid:
        if all(
            [
                grid.get((nx, ny)) == "#"
                for nx, ny in [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            ]
        ):
            inters.append((x, y))
    return sum([x * y for x, y in inters])


R = "R"
L = "L"

# NOTE: p2 only works using python2, not python3 - TODO look into this
def p2(prog):
    # hand-transcribed T_T
    path = eval(
        """[L,10,R,12,R,12,R,6,R,10,L,10,L,10,R,12,R,12,R,10,L,10,L,12,R,6,R,6,
        R,10,L,10,R,10,L,10,L,12,R,6,R,6,R,10,L,10,R,10,L,10,L,12,R,6,L,10,R,
        12,R,12,R,10,L,10,L,12,R,6]"""
    )
    ipath = []
    for e in path:
        if isinstance(e, int):
            ipath += [1 for _ in range(e)]
        else:
            ipath.append(e)
    pairs = []
    for i in range(0, len(path), 2):
        pairs.append(tuple(path[i : i + 2]))
    uqpairs = list(set(pairs))
    encoding = []
    for p in pairs:
        encoding.append(uqpairs.index(p))
    """
    print(encoding)
    [2, 0, 0, 4, 1, 2, 2, 0, 0, 1, 2, 3, 4, 4, 1, 2, 1, 2, 3, 4, 4, 1, 2,
     1, 2, 3, 4, 2, 0, 0, 1, 2, 3, 4]
    """
    # these were done by hand as well
    A = [2, 0, 0]
    B = [4, 1, 2]
    C = [1, 2, 3, 4]
    main = ["A", "B", "A", "C", "B", "C", "B", "C", "A", "C"]
    # enter input to program
    _in = ",".join(main) + "\n"
    for proc in (A, B, C):
        pairs = ["{},{}".format(*uqpairs[i]) for i in proc]
        _in += ",".join(pairs) + "\n"
    _in += "n\n"
    ord_in = [ord(i) for i in _in]
    prog[0] = 2
    out = execute_collect(prog, ord_in)
    return out[-1]


def main():
    tests()
    with open("in.txt", "r") as f:
        prog = [int(i) for i in f.readlines()[0].split(",")]
        assert p1(prog[:]) == 3888
        assert p2(prog[:]) == 927809


if __name__ == "__main__":
    main()
