serial = 6303


def power_level(x, y, s):
    return (((((x + 10) * y) + s) * (x + 10)) // 100) % 10 - 5


def power_level_square(_x, _y):
    level = 0
    for x in range(_x, _x + 3):
        for y in range(_y, _y + 3):
            level += power_level(x, y, serial)
    return level


assert power_level(3, 5, 8) == 4
assert power_level(122, 79, 57) == -5
assert power_level(217, 196, 39) == 0
assert power_level(101, 153, 71) == 4


best_level = float('-inf')
best_coords = None, None
for x in range(1, 298):
    for y in range(1, 298):
        level = power_level_square(x, y)
        if level > best_level:
            best_level = level
            best_coords = x, y

# Part 1
print(best_coords)
