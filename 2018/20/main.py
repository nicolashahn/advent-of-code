from collections import defaultdict
from pprint import pprint


DIR_VEC_MAP = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
}


def parse(line):
    ret = []
    while line:
        c = line.pop(0)
        if c == ')':
            return ret
        elif c == '(':
            ret.append(parse(line))
        else:
            ret.append(c)
    return ret


def walk(start_xy, dirs, doors):
    xy = start_xy
    for d in dirs:
        if isinstance(d, list):
            for new_dirs in d:
                walk(xy, new_dirs, doors)
        elif d in DIR_VEC_MAP:
            x, y = xy
            xv, yv = DIR_VEC_MAP[d]
            new_xy = (x + xv), (y + yv)
            doors[xy].append(new_xy)
            xy = new_xy


def get_dists(start_xy, doors):
    queue = [(start_xy, 0)]
    seen = set()
    dists = {start_xy: 0}
    while queue:
        xy, curr_dist = queue.pop(0)
        if xy not in dists:
            dists[xy] = curr_dist
        dists[xy] = min(curr_dist, dists[xy])
        if xy not in seen:
            seen.add(xy)
            for nxy in doors[xy]:
                queue.append((nxy, dists[xy] + 1))
    return dists


def get_dists_from_line(line):
    line = list(
        line[1:-1]
        .replace('(', '((')
        .replace(')', '))')
        .replace('|', ')('))
    dirs = parse(line)
    doors = defaultdict(list)
    walk((0, 0), dirs, doors)
    return get_dists((0, 0), doors)


with open('in.txt', 'r') as f:
    line = f.readlines()[0].strip()
    dists = get_dists_from_line(line)
    # Part 1
    print(max(dists.values()))
    # Part 2
    print(len([x for x in dists.values() if x >= 1000]))
