import re
import os
import matplotlib.pyplot as plt
import numpy as np

PLOT_DIR = 'plot/'


def parse_line(line):
    match_split = re.split(r'\<([^=]*)\>', line)
    pstr, vstr = match_split[1], match_split[3]
    return tuple(tuple(int(x) for x in xstr.split(','))
                 for xstr in (pstr, vstr))


def write_grid(vecs, file_num):
    positions = [pos for pos, vel in vecs]
    plt.scatter(*zip(*positions), marker="s")
    plt.savefig(
        os.path.join(PLOT_DIR, str(file_num) + '.png')
    )
    plt.gcf().clear()


def step(vecs, steps, multiplier=1):
    new_vecs = vecs
    for _ in range(steps):
        new_vecs = [
            (
                (
                    pos[0] + vel[0] * multiplier,
                    pos[1] + vel[1] * multiplier
                ),
            vel)
            for pos, vel in new_vecs
        ]
    return new_vecs


def bounding_box_size(vecs):
    max_x = max(v[0][0] for v in vecs)
    min_x = min(v[0][0] for v in vecs)
    max_y = max(v[0][1] for v in vecs)
    min_y = min(v[0][1] for v in vecs)
    return max_x - min_x + max_y - min_y


# Part 1 message happens on second 10519, which is the answer for part 2
with open('in.txt', 'r') as f:
    lines = f.readlines()
    vecs = [parse_line(line) for line in lines]
    # Did some experimentation by hand to get this far
    vecs = step(vecs, 1, 10510)
    for s in range(20):
        vecs = step(vecs, 1, 1)
        write_grid(vecs, s)
