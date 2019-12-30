def cut(deck, i):
    return deck[i:] + deck[:i]


assert cut(list(range(10)), 3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
assert cut(list(range(10)), -4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]


def deal_inc(deck, i):
    N = len(deck)
    ndeck = [None] * N
    ni = 0
    for c in deck:
        assert ndeck[ni] is None
        ndeck[ni] = c
        ni = (ni + i) % N
    return ndeck


deck = deal_inc(list(range(10)), 7)
deck = deal_inc(deck, 7)


assert deal_inc(list(range(10)), 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]


def deal_new(deck):
    return deck[::-1]


def cut_p(d, i, p):
    cut_point = d - i
    return (p - cut_point) % d


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist for a={},m={}".format(a, m))
    else:
        return x % m


def deal_inc_p(d, i, p):
    a = i
    m = d
    x = modinv(a, m)
    return (p * x) % m


def deal_new_p(d, p):
    return d - p - 1


def shuffle(actions, deck):
    for a in actions:
        if a.startswith("cut"):
            i = int(a.split()[-1])
            deck = cut(deck, i)
        elif a.startswith("deal with increment"):
            i = int(a.split()[-1])
            deck = deal_inc(deck, i)
        elif a.startswith("deal into new stack"):
            deck = deal_new(deck)
        else:
            raise ValueError
    return deck


def shuffle_rev(actions, p, d):
    for a in actions[::-1]:
        if a.startswith("cut"):
            i = int(a.split()[-1])
            p = cut_p(d, i, p)
        elif a.startswith("deal with increment"):
            i = int(a.split()[-1])
            p = deal_inc_p(d, i, p)
        elif a.startswith("deal into new stack"):
            p = deal_new_p(d, p)
        else:
            raise ValueError
    return p


test_actions = ["cut 3", "deal with increment 7", "deal into new stack", "cut 4"]
d = 11
for i in range(d):
    assert shuffle(test_actions, list(range(d)))[i] == shuffle_rev(test_actions, i, d)


def p1(actions, decksize):
    deck = list(range(decksize))
    deck = shuffle(actions, deck)
    return deck.index(2019)


def p2(actions, decksize, repeat):
    p = 2020
    for _ in range(repeat):
        p = shuffle_rev(actions, p, decksize)
    return p


def main():
    with open("in.txt", "r") as f:
        actions = f.read().strip().split("\n")
        assert p1(actions, 10007) == 2519
        # decksize = 119315717514047
        # repeat = 101741582076661
        # print(p2(actions, decksize, repeat))


if __name__ == "__main__":
    main()
