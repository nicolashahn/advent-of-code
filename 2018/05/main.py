import string

lu_pairs = [''.join(lu) for lu in zip(string.ascii_lowercase, string.ascii_uppercase)]
ul_pairs = [''.join(reversed(lu)) for lu in lu_pairs]
pairs = set(lu_pairs + ul_pairs)

with open('in.txt', 'r') as f:
    polymer = f.read()
    while any([pair in polymer for pair in pairs]):
        for pair in pairs:
            polymer = polymer.replace(pair,'')
    # Part 1
    print(len(polymer))
