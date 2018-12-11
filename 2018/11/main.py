from tqdm import tqdm


SERIAL = 6303
# SERIAL = 18

GRID_SIZE = 300


def power_level(x, y, s):
    return (((((x + 10) * y) + s) * (x + 10)) // 100) % 10 - 5


assert power_level(3, 5, 8) == 4
assert power_level(122, 79, 57) == -5
assert power_level(217, 196, 39) == 0
assert power_level(101, 153, 71) == 4
assert power_level(300, 300, 18) == 0
assert power_level(299, 300, 18) == 3


def power_level_square(_x, _y, size=3):
    level = 0
    for x in range(_x, _x + size):
        for y in range(_y, _y + size):
            level += power_level(x, y, SERIAL)
    return level


def best_size_for_coords(x, y, grid):
    largest = min(GRID_SIZE - x, GRID_SIZE - y)
    levels = []
    for size in range(largest):
        bot_right = grid[y + size][x + size]
        sum_horiz = sum(grid[y + size][x:x + size])
        sum_vert = sum([grid[_y][x + size] for _y in range(y, y + size)])
        last_level = levels[-1] if levels else 0
        level = last_level + sum_horiz + sum_vert + bot_right
        levels.append(level)
    best_size = levels.index(max(levels)) + 1
    return max(levels), best_size


best_power = float('-inf')
best_coords = None, None
for x in range(1, GRID_SIZE - 2):
    for y in range(1, GRID_SIZE - 2):
        power = power_level_square(x, y)
        if power > best_power:
            best_power = power
            best_coords = x, y

# Part 1
print(best_coords)


grid = []
for y in range(1, GRID_SIZE + 1):
    grid.append([])
    for x in range(1, GRID_SIZE + 1):
        grid[y - 1].append(power_level(x, y, SERIAL))

best_power = float('-inf')
best_coords = None, None, None
for x in tqdm(range(GRID_SIZE)):
    for y in range(GRID_SIZE):
        power, size = best_size_for_coords(x, y, grid)
        if power > best_power:
            best_power = power
            best_coords = x+1, y+1, size
            print('new best power: {} at {}'.format(best_power, best_coords))

# Part 2
print(best_coords)
