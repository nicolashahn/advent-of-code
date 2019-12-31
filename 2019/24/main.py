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


# number of levels above and below the initial one we will generate grids for
MAX_LVL = 200


class Grid:
    """
    Grid as a node in a doubly linked list allowing traversal to outer or inner
    grids.
    """

    def __init__(self, start_raw=None, up=None, down=None, level=0):
        self.grid = parse(
            start_raw
            or """.....
.....
.....
.....
....."""
        )
        mx, my = self.mid_cell
        self.grid[my][mx] = "?"
        self.up_grid = up
        self.down_grid = down
        self.ngrid_computed = False
        self.level = level

    @property
    def up(self):
        """ Get or create the Grid above this one in the recursive structure """
        if not self.up_grid:
            self.up_grid = Grid(down=self, level=self.level - 1)
        return self.up_grid

    @property
    def down(self):
        """ Get or create the Grid below this one in the recursive structure """
        if not self.down_grid:
            self.down_grid = Grid(up=self, level=self.level + 1)
        return self.down_grid

    @property
    def mid_cell(self):
        """ x,y coord of cell in middle of grid (representing inner/down grid) """
        return len(self.grid[0]) // 2, len(self.grid) // 2

    def is_outer_cell(self, x, y):
        """ Coordinate is on the outer edge of the grid """
        return (
            x == 0
            or y == 0
            or (x == len(self.grid[0]) - 1)
            or (y == len(self.grid) - 1)
        )

    def get_new_cell(self, x, y):
        """ Get new value of cell at x,y """
        raw_adjs = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        adj_living = 0
        for rx, ry in raw_adjs:
            if (
                (rx, ry) != self.mid_cell
                and 0 <= rx < len(self.grid[0])
                and 0 <= ry < len(self.grid)
            ):
                adj_living += 1 if self.grid[ry][rx] == "#" else 0
            else:
                if self.is_outer_cell(x, y):
                    ux, uy = self.up.mid_cell
                    if rx < 0:
                        adj_living += 1 if self.up.grid[uy][ux - 1] == "#" else 0
                    if rx == len(self.up.grid[0]):
                        adj_living += 1 if self.up.grid[uy][ux + 1] == "#" else 0
                    if ry < 0:
                        adj_living += 1 if self.up.grid[uy - 1][ux] == "#" else 0
                    if ry == len(self.up.grid):
                        adj_living += 1 if self.up.grid[uy + 1][ux] == "#" else 0
                elif (rx, ry) == self.mid_cell:
                    if x > rx:
                        adj_living += len([1 for r in self.down.grid if r[-1] == "#"])
                    elif x < rx:
                        adj_living += len([1 for r in self.down.grid if r[0] == "#"])
                    if y > ry:
                        adj_living += len([1 for c in self.down.grid[-1] if c == "#"])
                    elif y < ry:
                        adj_living += len([1 for c in self.down.grid[0] if c == "#"])
        cell_alive = self.grid[y][x] == "#"
        if (cell_alive and adj_living == 1) or (
            (not cell_alive) and adj_living in (1, 2)
        ):
            return "#"
        return "."

    def step(self):
        """
        Compute the new cell values (as ngrid), then ensure all levels above and below
        are computed, then set self.grid = ngrid.
        """
        ngrid = [["." for _ in row] for row in self.grid]
        for y, row in enumerate(self.grid):
            for x, _ in enumerate(row):
                if (x, y) != self.mid_cell:
                    ngrid[y][x] = self.get_new_cell(x, y)
                else:
                    ngrid[y][x] = "?"
        self.ngrid_computed = True
        if self.up_grid and self.level > -MAX_LVL:
            if not self.up.ngrid_computed:
                self.up.step()
        if self.down_grid and self.level < MAX_LVL:
            if not self.down.ngrid_computed:
                self.down.step()
        self.grid = ngrid
        self.ngrid_computed = False

    def count_bugs(self):
        """ Count sum of bug ('#') cells for this grid (not above or below grids) """
        return len([1 for c in "".join("".join(r) for r in self.grid) if c == "#"])


def test_Grid():
    testgrid = Grid(start_raw=test_in)
    assert testgrid.count_bugs() == 8
    testgrid.step()
    testgrid2 = Grid(start_raw=test_in2)
    assert testgrid2.grid == testgrid.grid
    for _ in range(9):
        testgrid.step()
    assert count_all_bugs(testgrid) == 99
    print("tests passed")


def count_all_bugs(grid):
    """ Count sum of the bugs in this grid and any connected grids above or below """
    t = grid.count_bugs()
    curr = grid
    for _ in range(MAX_LVL):
        curr = curr.up
        t += curr.count_bugs()
    curr = grid
    for _ in range(MAX_LVL):
        curr = curr.down
        t += curr.count_bugs()
    return t


def p2(raw):
    basegrid = Grid(start_raw=raw)
    for _ in range(200):
        basegrid.step()
    return count_all_bugs(basegrid)


def main():
    test_Grid()
    raw = """
#..#.
#.#.#
...#.
....#
#.#.#""".strip()
    assert p1(raw) == 12531574
    assert p2(raw) == 2033


if __name__ == "__main__":
    main()
