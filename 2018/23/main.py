import re
import sys
from z3 import If, Int, Ints, Optimize, Sum, solve
# import random

sys.setrecursionlimit(9000)


def make_nb(line):
    """ returns ((x, y, z), radius) """
    pos_re = re.search('\<(.+)\>', line)
    pos = [int(x) for x in pos_re.groups()[0].split(',')]
    rad_re = re.search('r\=(\d+)', line)
    rad = int(rad_re.groups()[0])
    return pos, rad


def dist(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def abs_sub_z3(x, y):
    sub = x - y
    return If(sub >= 0, sub, -sub)


def dist_z3(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return abs_sub_z3(x1, x2) + abs_sub_z3(y1, y2) + abs_sub_z3(z1, z2)


def num_in_range(pos, nbs, rad=None):
    x, y, z = pos
    return len([nb for nb in nbs
                if dist(pos, nb[0]) <= (rad if rad else nb[1])])


def num_in_range_z3(pos, nbs):
    x, y, z = pos
    return len([nb for nb in nbs
                if dist_z3(pos, nb[0]) <= nb[1]])


def in_range_z3(pos, nb):
    nbpos, r = nb
    return dist_z3(pos, nbpos) <= r


def p1(lines):
    nbs = [make_nb(l) for l in lines]
    strongest = max(nbs, key=lambda n: n[1])
    s_pos, s_rad = strongest
    print(num_in_range(s_pos, nbs, rad=s_rad))


def search_x_dim(nbs, minx, maxx):
    """
    If y and z are fixed at zero, find the x coordinate that maximizes
    number of bots in range, then minimizes distance to 0 from the set of
    coordinate that maximize number of bots in range.
    """
    y = z = 0
    steps = 2
    step_size = (maxx - minx // steps)

    # find a coord that gives the best num_in_range
    while step_size >= 1:
        best_num = 0
        for low_x in range(minx, maxx + 1, step_size):
            x = low_x + (step_size // 2)
            pos = (x, y, z)
            num = num_in_range(pos, nbs)
            if num > best_num:
                best_num = num
                best_low_x = low_x
        minx = best_low_x
        maxx = minx + step_size
        step_size //= steps
        print(minx, best_num, step_size)

    # then walk towards origin until not in best_num range
    x = minx
    step_size = abs(x - 0) // steps
    step_size = step_size if x > 0 else -(step_size)
    while abs(step_size) >= 1:
        if num_in_range((x - step_size, y, z), nbs) >= best_num:
            x -= step_size
        else:
            step_size //= steps
    return x


def search(nbs, minx, maxx, miny, maxy, minz, maxz):
    """
    Three-dimensional binary search to find a region reachable by the maximum
    number of nanobots, followed by another binary search to find the closest
    coordinate to origin in that region.
    """
    steps = 11
    step_size_x = (maxx - minx // steps)
    step_size_y = (maxy - miny // steps)
    step_size_z = (maxz - minz // steps)

    best_num = 0
    lowest_sum = float('inf')
    while step_size_x > 1 and step_size_y > 1 and step_size_z > 1:
        best_low_x = minx
        best_low_y = miny
        best_low_z = minz

        for low_x in range(minx, maxx + 1, step_size_x):
            x = low_x + (step_size_x // 2)
            # x = random.randrange(low_x, low_x + step_size_x)

            for low_y in range(miny, maxy + 1, step_size_y):
                y = low_y + (step_size_y // 2)
                # y = random.randrange(low_y, low_y + step_size_y)

                for low_z in range(minz, maxz + 1, step_size_z):
                    z = low_z + (step_size_z // 2)
                    # z = random.randrange(low_z, low_z + step_size_z)

                    pos = x, y, z
                    # print(pos, best_num)
                    num = num_in_range(pos, nbs)
                    if num > best_num or (
                            num == best_num and sum((x, y, z)) < lowest_sum):
                        if sum((x, y, z)) < lowest_sum:
                            lowest_sum = min(lowest_sum, sum((x, y, z)))
                        best_num = num
                        best_low_x = low_x
                        best_low_y = low_y
                        best_low_z = low_z
                        print(best_num, lowest_sum, (x, y, z))

        minz = best_low_z
        maxz = minz + step_size_z

        miny = best_low_y
        maxy = miny + step_size_y

        minx = best_low_x
        maxx = minx + step_size_x

        step_size_x //= steps
        step_size_y //= steps
        step_size_z //= steps

    # now minx, miny, minz are a coordinate that gives the highest discovered
    # num_in_range, need to walk towards the origin to find the coordinate in
    # this "best_num cloud" that has the lowest manhattan dist to origin

    # then walk towards origin until at the edge of best_num cloud
    x = minx
    y = miny
    z = minz

    best_x = best_y = best_z = float('inf')

    while abs(x) < abs(best_x) or abs(y) < abs(best_y) or abs(z) < abs(best_z):
        best_x, best_y, best_z = x, y, z

        step_size_x = abs(x - 0) // steps
        step_size_x = step_size_x if x > 0 else -(step_size_x)
        while abs(step_size_x) >= 1:
            if num_in_range((x - step_size_x, y, z), nbs) >= best_num:
                x -= step_size_x
            else:
                step_size_x //= steps

        step_size_y = abs(y - 0) // steps
        step_size_y = step_size_y if y > 0 else -(step_size_y)
        while abs(step_size_y) >= 1:
            if num_in_range((x, y - step_size_y, z), nbs) >= best_num:
                y -= step_size_y
            else:
                step_size_y //= steps

        step_size_z = abs(z - 0) // steps
        step_size_z = step_size_z if z > 0 else -(step_size_z)
        while abs(step_size_z) >= 1:
            if num_in_range((x, y, z - step_size_z), nbs) >= best_num:
                z -= step_size_z
            else:
                step_size_z //= steps

    # Best found so far manually:
    # (Pdb) num_in_range((18488882, 11656388, 15564375), nbs)
    # 917
    # >>> sum((18488882, 11656388, 15564375))
    # 45709645
    return (x, y, z), best_num


def p2(lines):
    nbs = [make_nb(l) for l in lines]

    x, y, z, part2 = Ints('x y z part2')
    coord = (x, y, z)
    opt = Optimize()

    cost = Sum([If(dist_z3(pos, coord) <= rad, 1, 0) for pos, rad in nbs])
    opt.maximize(cost)
    origin = (0, 0, 0)
    opt.minimize(dist_z3(coord, origin))
    opt.check()
    model = opt.model()

    # Part 2
    solve(dist_z3(origin, (model[x], model[y], model[z])) == part2)


# This part was an attempt to search the space with more and more
# granularity until we found a region of possible max num bots in range.
# Didn't work out but I want to leave this code in because it's still kind
# of cool and may be useful if I need multidimensional search for some
# other task.

# def p2(lines):
    # minx_nb = min(nbs, key=lambda n: n[0][0])
    # minx, _, _ = minx_nb[0]
    # miny_nb = min(nbs, key=lambda n: n[0][1])
    # _, miny, _ = miny_nb[0]
    # minz_nb = min(nbs, key=lambda n: n[0][2])
    # _, _, minz = minz_nb[0]
    # maxx_nb = max(nbs, key=lambda n: n[0][0])
    # maxx, _, _ = maxx_nb[0]
    # maxy_nb = max(nbs, key=lambda n: n[0][1])
    # _, maxy, _ = maxy_nb[0]
    # maxz_nb = max(nbs, key=lambda n: n[0][2])
    # _, _, maxz = maxz_nb[0]
    # # print(minx, miny, minz)
    # # print(maxx, maxy, maxz)
    # # x = search_x_dim(nbs, minx, maxx)
    # # print(x)
    # # __import__('pdb').set_trace()
    # xyz, num = search(nbs, minx, maxx, miny, maxy, minz, maxz)
    # x, y, z = xyz
    # print(xyz, num)
    # print(dist(xyz, (0,0,0)))


with open('in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
    p2(lines)
