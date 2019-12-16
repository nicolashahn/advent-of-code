def phase(seq):
    out = ""
    for i, s1 in enumerate(seq):
        i += 1
        pat = [0] * i + [1] * i + [0] * i + [-1] * i
        pat = pat[1:] + pat[:1]
        pi = 0
        t = 0
        for si2, s2 in enumerate(seq):
            t += int(s2) * pat[pi]
            pi = (pi + 1) % len(pat)
        out += str(abs(t) % 10)
    return out


def p1(seq, phases):
    for i in range(phases):
        seq = phase(seq)
    return seq[:8]


assert p1("12345678", 1) == "48226158"
assert p1("12345678", 4) == "01029498"
assert p1("80871224585914546619083218645595", 100) == "24176176"


def main():
    with open("in.txt", "r") as f:
        seq = f.read().strip()
        print(p1(seq, 100))


if __name__ == "__main__":
    main()
