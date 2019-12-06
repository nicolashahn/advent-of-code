def read_op(op):
    op = str(op).zfill(5)
    # True means positional (address) value, False means immediate
    positionals = [op[i] == "0" for i in range(3)][::-1]
    opcode = int(op[-2:])
    return opcode, positionals


def execute(prog, _input):
    output = []
    i = 0
    history = []
    while i < len(prog):
        history.append(i)
        opcode, poss = read_op(prog[i])
        if opcode == 1:
            a, b = [
                prog[prog[i + 1]] if poss[0] else prog[i + 1],
                prog[prog[i + 2]] if poss[1] else prog[i + 2],
            ]
            prog[prog[i + 3]] = a + b
            i += 4
        elif opcode == 2:
            a, b = [
                prog[prog[i + 1]] if poss[0] else prog[i + 1],
                prog[prog[i + 2]] if poss[1] else prog[i + 2],
            ]
            prog[prog[i + 3]] = a * b
            i += 4
        elif opcode == 3:
            a = prog[i + 1] if poss[0] else i + 1
            prog[a] = _input.pop()
            i += 2
        elif opcode == 4:
            a = prog[prog[i + 1]] if poss[0] else prog[i + 1]
            output.append(a)
            i += 2
        elif opcode == 5:
            a, b = [
                prog[prog[i + 1]] if poss[0] else prog[i + 1],
                prog[prog[i + 2]] if poss[1] else prog[i + 2],
            ]
            if a != 0:
                i = b
            else:
                i += 3
        elif opcode == 6:
            a, b = [
                prog[prog[i + 1]] if poss[0] else prog[i + 1],
                prog[prog[i + 2]] if poss[1] else prog[i + 2],
            ]
            if a == 0:
                i = b
            else:
                i += 3
        elif opcode == 7:
            a, b = [
                prog[prog[i + 1]] if poss[0] else prog[i + 1],
                prog[prog[i + 2]] if poss[1] else prog[i + 2],
            ]
            prog[prog[i + 3]] = 1 if a < b else 0
            i += 4
        elif opcode == 8:
            a, b = [
                prog[prog[i + 1]] if poss[0] else prog[i + 1],
                prog[prog[i + 2]] if poss[1] else prog[i + 2],
            ]
            prog[prog[i + 3]] = 1 if a == b else 0
            i += 4
        elif opcode == 99:
            break
        else:
            print(
                "execute() is broken, history of instruction positions: {}".format(
                    history
                )
            )
            __import__("pdb").set_trace()
    return output


def tests():
    # check equality w/position mode (opcode 8)
    assert execute([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8]) == [1]
    assert execute([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [7]) == [0]
    # check less than w/position mode (opcode 7)
    assert execute([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7]) == [1]
    assert execute([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8]) == [0]
    # check equality w/immediate mode (opcode 8)
    assert execute([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8]) == [1]
    assert execute([3, 3, 1108, -1, 8, 3, 4, 3, 99], [7]) == [0]
    # check less than w/position mode (opcode 7)
    assert execute([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7]) == [1]
    assert execute([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8]) == [0]
    # jump tests
    assert execute([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0]) == [
        0
    ]
    assert execute([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [5]) == [
        1
    ]
    assert execute([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]) == [0]
    assert execute([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [1]) == [1]
    # longer example from problem description
    long_prog = eval(
        """[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]"""
    )
    assert execute(long_prog[:], [7]) == [999]
    assert execute(long_prog[:], [8]) == [1000]
    assert execute(long_prog[:], [9]) == [1001]
    print("tests passed")


def main():
    tests()
    with open("in.txt", "r") as f:
        prog = [int(i) for i in f.readlines()[0].split(",")]
        # print(execute(prog[:], [1]))
        print(execute(prog[:], [5]))


if __name__ == "__main__":
    main()
