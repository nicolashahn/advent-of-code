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
    streaks = []
    curr = 1
    for i, d in enumerate(sn[:-1]):
        if d > sn[i + 1]:
            return False
        if d == sn[i + 1]:
            curr += 1
        else:
            streaks.append(curr)
            curr = 1
    streaks.append(curr)
    return 2 in streaks


def num_pws(lo, hi, pw_f):
    ct = 0
    for n in range(lo, hi + 1):
        ct += 1 if pw_f(n) else 0
    return ct


def main():
    lo, hi = [int(p) for p in "124075-580769".split("-")]
    print(num_pws(lo, hi, is_pw1))  # ans = 2150
    print(num_pws(lo, hi, is_pw2))  # ans = 1462


if __name__ == "__main__":
    main()
