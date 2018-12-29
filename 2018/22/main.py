import heapq


# input:
DEPTH = 11541
TARGET_XY = 14, 778

# example input:
# DEPTH = 510
# TARGET_XY = 10, 10

# memoization for erosion
MEMO = {}

# how far we can go past the TARGET_XY in both x and y dimensions
EXTRA = 30

# region types
ROCKY = 0
WET = 1
NARROW = 2

# mapping from type value to display character
TYPE_MAP = {
    ROCKY: '.',
    WET: '=',
    NARROW: '|',
}

# possible equipment
TORCH = 'torch'
CGEAR = 'climbing_gear'
NEITHER = 'neither'

TOOLS = (TORCH, CGEAR, NEITHER)

# allowed tools for each region
TOOL_MAP = {
    ROCKY: set((TORCH, CGEAR)),
    WET: set((CGEAR, NEITHER)),
    NARROW: set((TORCH, NEITHER)),
}


def display(path=[]):
    tx, ty = TARGET_XY
    out = ['\n']
    for y in range(ty + EXTRA):
        for x in range(tx + EXTRA):
            if (x, y) == TARGET_XY:
                char = 'T'
            elif (x, y) in path:
                char = 'X'
            else:
                char = TYPE_MAP[get_type(x, y)]
            out.append(char)
        out.append('\n')
    print(''.join(out))


def get_erosion(x, y):
    if (x, y) not in MEMO:
        gi = None
        if (x, y) == (0, 0) or (x, y) == TARGET_XY:
            gi = 0
        elif x == 0:
            gi = 48271 * y
        elif y == 0:
            gi = 16807 * x
        else:
            gi = get_erosion(x, y - 1) * get_erosion(x - 1, y)
        erosion = (gi + DEPTH) % 20183
        MEMO[(x, y)] = erosion
    return MEMO[(x, y)]


def get_type(x, y):
    return get_erosion(x, y) % 3


def get_adjs(x, y):
    adjs = []
    tx, ty = TARGET_XY
    for nx, ny in (
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ):
        if nx >= 0 and ny >= 0 and nx < tx + EXTRA and ny < ty + EXTRA:
            adjs.append((nx, ny))
    return adjs


def get_next_cost_actions(cost_action):
    cost, action = cost_action
    xy, tool = action
    actions = []
    for newtool in TOOLS:
        if newtool != tool:
            action = (cost + 7, (xy, newtool))
            actions.append(action)
    for adj in get_adjs(*xy):
        if tool in TOOL_MAP[get_type(*adj)] and tool in TOOL_MAP[get_type(*xy)]:
            action = (cost + 1, (adj, tool))
            actions.append(action)
    return actions


def djikstra():
    # nodes are (cost, ((x, y), tool)
    start = (0, ((0, 0), TORCH))
    frontier = [start]
    visited = set()
    parents = {start: None}

    while frontier:
        cost_action = heapq.heappop(frontier)
        cost, action = cost_action
        xy, tool = action
        if action not in visited:
            visited.add(action)
            if action == (TARGET_XY, TORCH):
                ca = cost_action
                path = [ca]
                while parents[ca]:
                    path.append(parents[ca])
                    ca = parents[ca]
                path_xys = [a[0] for c, a in path]
                display(path=path_xys)
                return cost
            for new_cost_action in get_next_cost_actions(cost_action):
                parents[new_cost_action] = cost_action
                heapq.heappush(frontier, new_cost_action)


def p1():
    tx, ty = TARGET_XY
    res = 0
    for x in range(tx + 1):
        for y in range(ty + 1):
            erosion = get_erosion(x, y)
            res += erosion % 3
    # display()
    return res


def p2():
    return djikstra()


print(p1())
print(p2())
