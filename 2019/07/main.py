from itertools import permutations


def read_op(op):
    op = str(op).zfill(5)
    # True means positional (address) value, False means immediate
    positionals = [op[i] == "0" for i in range(3)][::-1]
    opcode = int(op[-2:])
    return opcode, positionals


def execute(prog, _input):
    prog = prog[:]
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


def amps(prog):
    combos = permutations([0, 1, 2, 3, 4], 5)
    best = 0
    for combo in combos:
        combo = list(combo)
        _in = [0]
        for _ in range(5):
            _in.append(combo.pop())
            _in = execute(prog, _in)
        best = max(best, _in[0])
    return best


def main():
    with open("in.txt", "r") as f:
        prog = [int(i) for i in f.readlines()[0].split(",")]
        print(amps(prog))


if __name__ == "__main__":
    main()
