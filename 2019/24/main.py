test_in = """....#
#..#.
#..##
..#..
#...."""
test_in2 = """#..#.
####.
###.#
##.##
.##.."""
test_in3 = """.....
.....
.....
#....
.#..."""


def parse(raw):
    return [list(l) for l in raw.split("\n")]


def unparse(grid):
    return "\n".join(["".join(row) for row in grid])


assert test_in == unparse(parse(test_in))


def get_score(raw):
    grid = parse(raw)
    i = 1
    score = 0
    for row in grid:
        for cell in row:
            if cell == "#":
                score += i
            i *= 2
    return score


assert get_score(test_in3) == 2129920


def get_new_cell(grid, x, y):
    adj_living = 0
    for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            adj_living += 1 if grid[ny][nx] == "#" else 0
    cell_alive = grid[y][x] == "#"
    if (cell_alive and adj_living == 1) or ((not cell_alive) and adj_living in (1, 2)):
        return "#"
    return "."


def step(grid):
    ngrid = [[None for _ in row] for row in grid]
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            ngrid[y][x] = get_new_cell(grid, x, y)
    return ngrid


assert step(parse(test_in)) == parse(test_in2)


def p1(raw):
    seen = set([raw])
    while True:
        raw = unparse(step(parse(raw)))
        if raw in seen:
            break
        seen.add(raw)
    return get_score(raw)


def main():
    raw = """
#..#.
#.#.#
...#.
....#
#.#.#""".strip()
    print(p1(raw))


if __name__ == "__main__":
    main()
