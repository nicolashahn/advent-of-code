
def addr(a, b, c, regs):
    regs[c] = regs[a] + regs[b]
    return regs


assert addr(0, 1, 2, [3, 4, 0, 0]) == [3, 4, 7, 0]


def addi(a, b, c, regs):
    regs[c] = regs[a] + b
    return regs


assert addi(0, 1, 2, [3, 4, 0, 0]) == [3, 4, 4, 0]


def mulr(a, b, c, regs):
    regs[c] = regs[a] * regs[b]
    return regs


assert mulr(0, 1, 2, [3, 4, 0, 0]) == [3, 4, 12, 0]


def muli(a, b, c, regs):
    regs[c] = regs[a] * b
    return regs


assert muli(0, 3, 2, [3, 4, 0, 0]) == [3, 4, 9, 0]


def banr(a, b, c, regs):
    regs[c] = regs[a] & regs[b]
    return regs


assert banr(0, 1, 2, [5, 3, 0, 0]) == [5, 3, 1, 0]


def bani(a, b, c, regs):
    regs[c] = regs[a] & b
    return regs


assert bani(0, 6, 2, [3, 3, 0, 0]) == [3, 3, 2, 0]


def borr(a, b, c, regs):
    regs[c] = regs[a] | regs[b]
    return regs


assert borr(0, 1, 2, [5, 2, 0, 0]) == [5, 2, 7, 0]


def bori(a, b, c, regs):
    regs[c] = regs[a] | b
    return regs


assert bori(0, 4, 2, [2, 2, 0, 0]) == [2, 2, 6, 0]


def setr(a, b, c, regs):
    regs[c] = regs[a]
    return regs


assert setr(0, 1, 2, [2, 3, 0, 0]) == [2, 3, 2, 0]


def seti(a, b, c, regs):
    regs[c] = a
    return regs


assert seti(5, 1, 2, [2, 3, 0, 0]) == [2, 3, 5, 0]


def gtir(a, b, c, regs):
    regs[c] = 1 if a > regs[b] else 0
    return regs


assert gtir(5, 1, 2, [2, 3, 0, 0]) == [2, 3, 1, 0]
assert gtir(0, 1, 2, [2, 3, 0, 0]) == [2, 3, 0, 0]


def gtri(a, b, c, regs):
    regs[c] = 1 if regs[a] > b else 0
    return regs


assert gtri(0, 1, 2, [2, 3, 0, 0]) == [2, 3, 1, 0]
assert gtri(0, 5, 2, [2, 3, 0, 0]) == [2, 3, 0, 0]


def gtrr(a, b, c, regs):
    regs[c] = 1 if regs[a] > regs[b] else 0
    return regs


assert gtrr(0, 1, 2, [2, 3, 0, 0]) == [2, 3, 0, 0]
assert gtrr(0, 1, 2, [4, 3, 0, 0]) == [4, 3, 1, 0]


def eqir(a, b, c, regs):
    regs[c] = 1 if a == regs[b] else 0
    return regs


assert eqir(0, 1, 2, [2, 3, 0, 0]) == [2, 3, 0, 0]
assert eqir(3, 1, 2, [4, 3, 0, 0]) == [4, 3, 1, 0]
assert eqir(2, 2, 2, [0, 0, 2, 3]) == [0, 0, 1, 3]


def eqri(a, b, c, regs):
    regs[c] = 1 if regs[a] == b else 0
    return regs


assert eqri(0, 1, 2, [2, 3, 0, 0]) == [2, 3, 0, 0]
assert eqri(0, 4, 2, [4, 3, 0, 0]) == [4, 3, 1, 0]
assert eqri(2, 2, 2, [0, 0, 2, 3]) == [0, 0, 1, 3]


def eqrr(a, b, c, regs):
    regs[c] = 1 if regs[a] == regs[b] else 0
    return regs


assert eqrr(0, 1, 2, [2, 3, 0, 0]) == [2, 3, 0, 0]
assert eqrr(0, 1, 2, [3, 3, 0, 0]) == [3, 3, 1, 0]


all_ops = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]


with open('in.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    total_ct = 0
    for i in range(0, 3160, 4):
        instruction = [int(c) for c in lines[i+1].split()]
        after = eval(lines[i+2][8:])
        valid_ops = []
        for op in all_ops:
            _, a, b, c = instruction
            before = eval(lines[i][8:])
            if op(a, b, c, before) == after:
                valid_ops.append(op.__name__)
        if len(valid_ops) >= 3:
            total_ct += 1
        # print(instruction, before, after)
        # print(valid_ops)

    # Part 1
    print(total_ct)

