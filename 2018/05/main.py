import string

lu_pairs = [''.join(lu) for lu in zip(string.ascii_lowercase, string.ascii_uppercase)]
ul_pairs = [''.join(reversed(lu)) for lu in lu_pairs]
pairs = set(lu_pairs + ul_pairs)

def reduce(_polymer):
    polymer = _polymer + ''
    while any([pair in polymer for pair in pairs]):
        for pair in pairs:
            polymer = polymer.replace(pair, '')
    return polymer


with open('in.txt', 'r') as f:
    polymer = f.read()
    reduced = len(reduce(polymer))
    # Part 1
    print(reduced)

    lens = []
    for pair in pairs:
        _polymer = polymer
        for char in pair:
            _polymer = _polymer.replace(char, '')
        lens.append(len(reduce(_polymer)))
    # Part 2 (pretty slow)
    print(min(lens))
