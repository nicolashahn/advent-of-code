#!/usr/bin/env python3
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from time import sleep


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


def intcode_tests():
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


# NOTE: Only python 3 compatible
class Buffer:
    def __init__(self, addr):
        self.addr = addr
        self.buf = deque([addr])

    def __repr__(self):
        return "<Buffer {}: {}>".format(self.addr, list(self.buf))

    def __iter__(self):
        return self

    def __next__(self):
        if self.buf:
            return self.buf.popleft()
        return -1

    def __len__(self):
        return len(self.buf)

    def push(self, val):
        self.buf.append(val)

    def is_empty(self):
        return len(self.buf) == 0


class NIC:
    def __init__(self, prog, addr, buffer_map):
        self.buffer_map = buffer_map
        buffer = buffer_map[addr]
        self.comp = execute(prog[:], buffer)

    def run(self):
        while True:
            addr = next(self.comp)
            x = next(self.comp)
            y = next(self.comp)
            print("sending to address {} values {}, {}".format(addr, x, y))
            # if addr == 255:
            #     print("ANSWER TO PART 1: {}".format(y))
            self.buffer_map[addr].push(x)
            self.buffer_map[addr].push(y)


def buffer_tests():
    b = Buffer(1)
    assert next(b) == 1
    b.push(2)
    assert next(b) == 2
    assert next(b) == -1


def p1(prog):
    N = 50
    buffers = {addr: Buffer(addr) for addr in range(N)}
    nics = [NIC(prog[:], addr, buffers) for addr in range(N)]
    with ThreadPoolExecutor(max_workers=50) as thread_exec:
        print("starting NIC execution...")
        futures = {}
        for i, nic in enumerate(nics):
            futures[i] = thread_exec.submit(nic.run)


class NAT:
    def __init__(self, buffer_map):
        self.bs = buffer_map
        self.buf = self.bs[255]
        self.history = []

    def run(self):
        print("NAT.run called")
        while True:
            if (
                all([b.is_empty() for i, b in self.bs.items() if i != 255])
                and len(self.buf) > 1
            ):
                while len(self.buf) > 2:
                    next(self.buf)
                print(self.buf)
                x = next(self.buf)
                y = next(self.buf)
                print("NAT sending {}, {}".format(x, y))
                if [x, y] == self.history[-2:]:
                    print("ANSWER TO PART 2: {}".format(y))
                self.history += [x, y]
                self.bs[0].push(x)
                self.bs[0].push(y)
            sleep(0.000000000001)


def p2(prog):
    N = 50
    buffers = {addr: Buffer(addr) for addr in range(N)}
    buffers[255] = Buffer(255)
    _ = next(buffers[255])  # throw away first input that NICs need but NAT doesn't
    nics = [NIC(prog[:], addr, buffers) for addr in range(N)]
    with ThreadPoolExecutor(max_workers=len(buffers)) as thread_exec:
        print("starting NIC execution...")
        futures = {}
        nat = NAT(buffers)
        futures[255] = thread_exec.submit(nat.run)
        for i, nic in enumerate(nics):
            futures[i] = thread_exec.submit(nic.run)


def main():
    intcode_tests()
    buffer_tests()
    with open("in.txt", "r") as f:
        prog = [int(i) for i in f.readlines()[0].split(",")]
        # print(p1(prog[:]))
        print(p2(prog[:]))


if __name__ == "__main__":
    main()
