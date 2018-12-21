def get_adjs(x, y, grid):
    adjs = []
    for ax, ay in (
        (x + 1, y),
        (x - 1, y),
        (x + 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x, y + 1),
        (x, y - 1),
    ):
        if (0 <= ax < len(grid[0])) and (0 <= ay < len(grid)):
            adjs.append(grid[ay][ax])
    return adjs


def step_cell(x, y, grid):
    adjs = get_adjs(x, y, grid)
    cell = grid[y][x]
    if cell == '.':
        if len([a for a in adjs if a == '|']) >= 3:
            return '|'
        else:
            return '.'
    elif cell == '|':
        if len([a for a in adjs if a == '#']) >= 3:
            return '#'
        else:
            return '|'
    elif cell == '#':
        if '|' in adjs and '#' in adjs:
            return '#'
        else:
            return '.'


def step_grid(grid):
    next_grid = [[None for _ in range(len(grid[0]))]
                 for _ in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            next_grid[y][x] = step_cell(x, y, grid)
    return next_grid


def get_score(grid):
    wooded = lumberyards = 0
    for row in grid:
        for cell in row:
            if cell == '|':
                wooded += 1
            elif cell == '#':
                lumberyards += 1
    return wooded * lumberyards


def p1(lines):
    last = 0
    grid = [line.strip() for line in lines]
    for _ in range(10):
        grid = step_grid(grid)
        # print('\n'.join([''.join(row) for row in grid]))
        score = get_score(grid)
        last = score
    print(last)


with open('in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
