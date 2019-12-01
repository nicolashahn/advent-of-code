def p1(ns):
    return sum([(i // 3) - 2 for i in ns])


assert p1([12]) == 2
assert p1([14]) == 2
assert p1([1969]) == 654
assert p1([100756]) == 33583


def main():
    with open("in.txt", "r") as f:
        print(p1([int(i) for i in f.readlines()]))


if __name__ == "__main__":
    main()
