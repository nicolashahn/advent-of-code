def is_pw1(n):
    sn = str(n)
    double = False
    for i, d in enumerate(sn[:-1]):
        if d == sn[i + 1]:
            double = True
        elif d > sn[i + 1]:
            return False
    return double


def is_pw2(n):
    sn = str(n)
    has2 = False
    curr = 1
    for i, d in enumerate(sn[:-1]):
        if d > sn[i + 1]:
            return False
        if d == sn[i + 1]:
            curr += 1
        else:
            has2 = curr == 2 or has2
            curr = 1
    return has2 or curr == 2


def num_pws(lo, hi, pw_f):
    return sum([1 if pw_f(n) else 0 for n in range(lo, hi + 1)])


def main():
    lo, hi = [int(p) for p in "124075-580769".split("-")]
    print(num_pws(lo, hi, is_pw1))  # ans = 2150
    print(num_pws(lo, hi, is_pw2))  # ans = 1462


if __name__ == "__main__":
    main()
