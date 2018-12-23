import re


def make_nb(line):
    """ returns ((x, y, z), radius) """
    pos_re = re.search('\<(.+)\>', line)
    pos = [int(x) for x in pos_re.groups()[0].split(',')]
    rad_re = re.search('r\=(\d+)', line)
    rad = int(rad_re.groups()[0])
    return pos, rad


def dist(nb1, nb2):
    pos1, _ = nb1
    pos2, _ = nb2
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def p1(lines):
    nbs = [make_nb(l) for l in lines]
    strongest = max(nbs, key=lambda n: n[1])
    _, s_rad = strongest
    ct = 0
    for nb in nbs:
        if dist(nb, strongest) <= s_rad:
            ct += 1
    print(ct)


with open('in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
