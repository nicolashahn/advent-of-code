def p1(ns):
    i = 0
    while ns[i] != 99:
        if ns[i] == 1:
            ns[ns[i + 3]] = ns[ns[i + 1]] + ns[ns[i + 2]]
        elif ns[i] == 2:
            ns[ns[i + 3]] = ns[ns[i + 1]] * ns[ns[i + 2]]
        elif ns[i] == 99:
            break
        i += 4
    return ns[0]


assert p1([1, 0, 0, 0, 99]) == 2
assert p1([1, 1, 1, 4, 99, 5, 6, 0, 99]) == 30
assert p1([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == 3500


def p2(ns):
    for n in range(100):
        for v in range(100):
            ns[1] = n
            ns[2] = v
            if p1(ns[:]) == 19690720:
                return str(n).zfill(2) + str(v).zfill(2)


def main():
    with open("in.txt", "r") as f:
        ns = [int(i) for i in f.readlines()[0].split(",")]
        # Need to read the instructions to the very end...
        ns[1] = 12
        ns[2] = 2
        # print(p1(ns))
        print(p2(ns))


if __name__ == "__main__":
    main()
