import math
from collections import Counter


def prod(rn, mat, store, g):
    """
    rn:    required number of material to produce
    mat:   desired material to produce
    store: global Counter of materials we already have (mutable)
    g:     global graph of ingredient requirements (immutable)

    return: number of ORE required
    """
    # number produced per batch, ingredient dict {material: # required}
    bn, ings = g[mat]
    # number of batches required to get to n materials
    b = math.ceil(float(rn - store[mat]) / float(bn))
    # base case, the single ingredient is ORE
    if len(ings) == 1 and "ORE" in ings:
        store[mat] += bn * b
        return ings["ORE"] * b
    # recursively produce intermediate materials until we have enough for b batches,
    # this is a while loop because producing one ingredient can use resources needed for
    # another
    ore = 0
    while any([store[imat] < ni * b for imat, ni in ings.items()]):
        for imat, ni in ings.items():
            if store[imat] < ni * b:
                ore += prod(ni * b, imat, store, g)
    # subtract ingredients from, add desired material to store
    for imat, ni in ings.items():
        store[imat] -= ni * b
    store[mat] += bn * b
    return ore


def p1(g):
    return prod(1, "FUEL", Counter(), g)


def p2(g):
    # number of FUEL we know we can produce
    base = 0
    # number of FUEL on top of base we're attempting to produce
    n = 1
    while True:
        ore = prod(base + n, "FUEL", Counter(), g)
        if ore > 1000000000000:
            if n == 1:
                break
            n = 1
        else:
            base += n
            n *= 2
    return base


def parse_pair(p):
    num, mat = p.strip().split()
    return int(num), mat


def parse_in(raw):
    # raw: {material: str: (# produced: int, ingredients)}
    # ingredients: [(# required: int, material: str)]
    g = {}
    for line in raw.split("\n"):
        left, right = line.split("=>")
        pairs = left.split(",")
        ings = {}
        for p in pairs:
            n, m = parse_pair(p)
            ings[m] = n
        num, res = parse_pair(right)
        g[res] = (num, ings)
    return g


def tests():
    assert p1(parse_in("""10 ORE => 1 FUEL""")) == 10
    assert (
        p1(
            parse_in(
                """10 ORE => 5 A
    10 A => 1 FUEL"""
            )
        )
        == 20
    )

    assert (
        p1(
            parse_in(
                """10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL"""
            )
        )
        == 31
    )

    assert (
        p1(
            parse_in(
                """9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL"""
            )
        )
        == 165
    )

    test_13312 = parse_in(
        """157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
    )
    assert p1(test_13312) == 13312

    test_180697 = parse_in(
        """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
    17 NVRVD, 3 JNWZP => 8 VPVL
    53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
    22 VJHF, 37 MNCFX => 5 FWMGM
    139 ORE => 4 NVRVD
    144 ORE => 7 JNWZP
    5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
    5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
    145 ORE => 6 MNCFX
    1 NVRVD => 8 CXFTF
    1 VJHF, 6 MNCFX => 4 RFSQX
    176 ORE => 6 VJHF"""
    )
    assert p1(test_180697) == 180697
    assert (
        p1(
            parse_in(
                """171 ORE => 8 CNZTR
    7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
    114 ORE => 4 BHXH
    14 VRPVC => 6 BMBT
    6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
    6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
    15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
    13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
    5 BMBT => 4 WPTQ
    189 ORE => 9 KTJDG
    1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
    12 VRPVC, 27 CNZTR => 2 XDBXC
    15 KTJDG, 12 BHXH => 5 XCVML
    3 BHXH, 2 VRPVC => 7 MZWV
    121 ORE => 7 VRPVC
    7 XCVML => 6 RJRHP
    5 BHXH, 4 VRPVC => 5 LTCX"""
            )
        )
        == 2210736
    )

    assert p2(test_13312) == 82892753
    print("tests completed")


def main():
    tests()
    with open("in.txt", "r") as f:
        g = parse_in(f.read().strip())
        assert p1(g) == 201324
        assert p2(g) == 6326857


if __name__ == "__main__":
    main()
