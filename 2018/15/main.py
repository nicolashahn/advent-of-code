import sys


ELF = 'E'
GOBLIN = 'G'
WALL = '#'
OPEN = '.'
RACES = (ELF, GOBLIN)
HP = 200
AP = 3


def m_dist(xy1, xy2):
    """ Manhattan distance. """
    x1, y1 = xy1
    x2, y2 = xy2
    return abs(x1 - x2) + abs(y1 - y2)


class Unit:
    """ Goblin or Elf unit. """

    def __init__(self, race, x, y):
        assert race in RACES
        self.race = race
        self.hp = HP
        self.ap = AP
        self.x = x
        self.y = y
        self.rounds = 0

    def __repr__(self):
        return "{}({})".format(self.race, self.hp)

    @property
    def alive(self):
        return self.hp > 0

    def hit(self, ap):
        self.hp -= ap

    @property
    def xy(self):
        return self.x, self.y

    @property
    def yx(self):
        """ Comparison property to get the list of units in reading order. """
        return self.y, self.x

    def move(self, newx, newy):
        self.x = newx
        self.y = newy
        self.rounds += 1


class Sim:
    """ Goblin vs Elf sim, holds state and methods for advancing state. """

    def __init__(self, lines):
        self.units, self.map = self.make_units_and_map(lines)
        self.rounds = 0

    def live_units(self, race=None):
        races = (race,) if race is not None else RACES
        return [unit for unit in self.units
                if unit.alive and unit.race in races]

    @property
    def has_ended(self):
        """ Check if all units of one type have been eliminated. """
        return not (self.live_units(GOBLIN) and self.live_units(ELF))

    def display(self):
        """ Print the map with goblins and elves overlayed. """
        to_display = []
        goblins = {unit.yx for unit in self.live_units(GOBLIN)}
        elves = {unit.yx for unit in self.live_units(ELF)}
        for y in range(len(self.map)):
            row_units = sorted(
                [unit for unit in self.live_units() if unit.y == y],
                key=lambda u: u.x
            )
            for x in range(len(self.map[0])):
                if (y, x) in goblins:
                    to_display.append(GOBLIN)
                elif (y, x) in elves:
                    to_display.append(ELF)
                else:
                    to_display.append(self.map[y][x])
            if row_units:
                to_display += list("   " + str(row_units))
            to_display.append("\n")
        print(''.join(to_display))

    @staticmethod
    def make_units_and_map(lines):
        """
        Take the raw input and split it into units and the underlying map.

        units:
            List of Units.
        map:
            Grid (list of strs (rows)) with the underlying map.
            (only '.' and '#')
        """
        units = []
        map = [list(line.strip()) for line in lines]
        for y in range(len(map)):
            for x in range(len(map[0])):
                tile = map[y][x]
                if tile in RACES:
                    unit = Unit(tile, x, y)
                    units.append(unit)
                    map[y][x] = '.'
        map = [''.join(row) for row in map]
        return units, map

    def run(self):
        """
        Run the simulation until all units of one type are eliminated.
        Returns the answer to part 1: (# of rounds * sum of HP of units left)
        """
        self.display()
        while True:
            ended = self.round()
            if ended:
                break
            self.rounds += 1
            print(self.rounds)
            self.display()
        self.display()
        hps = sum([unit.hp for unit in self.live_units()])
        return hps * self.rounds

    def round(self):
        """
        All units move and attack once. Updates self.units and increments
        self.rounds. Returns whether the simulation has ended this round.
        """
        ordered_units = sorted(self.live_units(), key=lambda u: u.yx)
        for unit in ordered_units:
            if unit.rounds <= self.rounds and unit.alive:
                self.move(unit)
                self.attack(unit)
            if self.has_ended:
                return True
        return False

    def move(self, unit):
        """
        Have a unit step towards the nearest enemy unit, update its coordinates
        in self.units.
        """
        if not self.adjacent_enemies(unit):
            in_range = self.get_in_range(unit)
            target_xy = self.get_target_tile(unit, in_range)
            if target_xy:
                next_step_xy = self.get_next_step(unit, target_xy)
                if next_step_xy:
                    unit.move(*next_step_xy)

    def adjacent_enemies(self, unit):
        """
        Return the enemy units adjacent to this unit.
        """
        enemy_race = GOBLIN if unit.race == ELF else ELF
        enemies = self.live_units(race=enemy_race)
        return [enemy for enemy in enemies
                if m_dist(enemy.xy, unit.xy) == 1]

    def get_in_range(self, unit):
        """
        Get all open coordinates adjacent to units that are enemies of the
        given unit.
        """
        enemy_race = GOBLIN if unit.race == ELF else ELF
        enemy_units = self.live_units(enemy_race)
        in_range = []
        for unit in enemy_units:
            in_range += self.get_open_adjacents(*unit.xy)
        return in_range

    def get_open_adjacents(self, _x, _y):
        """
        Get list of coordinates both open and adjacent to the given coordinate.
        """
        live_unit_coords = {unit.xy for unit in self.live_units()}
        adjacents = []
        for x, y in (
            (_x, _y - 1),
            (_x - 1, _y),
            (_x, _y + 1),
            (_x + 1, _y),
        ):
            if (
                x >= 0 and
                y >= 0 and
                x < len(self.map[0]) and
                y < len(self.map)
            ):
                if self.map[y][x] == OPEN and (x, y) not in live_unit_coords:
                    adjacents.append((x, y))
        return adjacents

    def get_target_tile(self, unit, in_range):
        """
        First finds reachable target coords via BFS, and selects the coord that
        is nearest in reading order.
        """
        if not in_range:
            return None

        queue = [(0, unit.xy)]
        seen = set()
        # list of (dist, (x, y))
        reachables = []

        while queue:
            dist, xy = queue.pop(0)
            if xy not in seen:
                seen.add(xy)
                if xy in in_range:
                    reachables.append((dist + 1, xy))
                adjs = self.get_open_adjacents(*xy)
                dist_adjs = [(dist + 1, adj) for adj in adjs]
                queue += dist_adjs

        sorted_reachables = sorted(reachables)
        nearests = [xy for d, xy in sorted_reachables
                    if d == sorted_reachables[0][0]]

        if nearests:
            nearests = self.sort_reading_order(nearests)
            xy = nearests[0]
            return xy

    @staticmethod
    def sort_reading_order(xys):
        return list(sorted(xys, key=lambda xy: (xy[1], xy[0])))

    def get_next_step(self, unit, target_xy):
        """
        Find the adjacent tile to the unit which is closest to the target tile.
        If there are multiple, return the first one in reading order.
        """
        possible_steps = self.get_open_adjacents(*unit.xy)
        dist_steps = sorted([(self.path_dist(target_xy, step), step)
                             for step in possible_steps])
        best_steps = [step for dist, step in dist_steps
                      if dist == dist_steps[0][0]]
        best_step = self.sort_reading_order(best_steps)[0]
        return best_step

    def path_dist(self, xy1, xy2):
        """
        Lenth of shortest path from first to second coord traveling through
        the map.
        """
        dists = {xy1: 0}
        queue = [xy1]
        seen = set()
        while queue:
            xy = queue.pop(0)
            if xy not in seen:
                seen.add(xy)
                for adj in self.get_open_adjacents(*xy):
                    if adj not in dists or dists[adj] > dists[xy] + 1:
                        dists[adj] = dists[xy] + 1
                    queue.append(adj)
        if xy2 in dists:
            return dists[xy2]
        return float('inf')

    def attack(self, unit):
        """
        Get enemies adjacent to this unit, and if there are any, attack the one
        with the lowest hp. Break a tie with reading order.
        """
        ordered_enemies = sorted(self.adjacent_enemies(unit),
                                 key=lambda e: (e.hp, e.yx))
        if ordered_enemies:
            ordered_enemies[0].hit(unit.ap)


def main():
    data = 'in.txt'
    if len(sys.argv) > 1:
        data = sys.argv[1]
    with open(data, 'r') as f:
        lines = f.readlines()
        sim = Sim(lines)
        result = sim.run()
        # Part 1
        print(result)


if __name__ == '__main__':
    main()
