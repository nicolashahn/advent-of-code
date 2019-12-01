def f(n):
    return n // 3 - 2


def p1(ns):
    return sum([f(i) for i in ns])


assert p1([12]) == 2
assert p1([14]) == 2
assert p1([1969]) == 654
assert p1([100756]) == 33583


def p2(ns):
    t = 0
    for n in ns:
        c = f(n)
        while c > 0:
            t += c
            c = f(c)
    return t


def main():
    with open("in.txt", "r") as f:
        ns = [int(i) for i in f.readlines()]
        print(p1(ns))
        print(p2(ns))


if __name__ == "__main__":
    main()
