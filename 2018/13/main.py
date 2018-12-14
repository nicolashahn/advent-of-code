# Possible turns
LEFT = 'LEFT'
STRAIGHT = 'STRAIGHT'
RIGHT = 'RIGHT'

TURNS = (LEFT, STRAIGHT, RIGHT)

# which way the car is facing, in vectors
NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

DIR_VEC_MAP = {
    '^': NORTH,
    '>': EAST,
    'v': SOUTH,
    '<': WEST,
}

REPLACE_CAR_MAP = {
    '^': '|',
    '>': '-',
    'v': '|',
    '<': '-',
}

CLOCKWISE_DIRS = tuple(DIR_VEC_MAP.keys())

# for the `/` char when deciding what our new direction will be
FWD_SLASH_MAP = {
    '^': '>',
    'v': '<',
    '>': '^',
    '<': 'v',
}

# for the `\` char when deciding what our new direction will be
BACK_SLASH_MAP = {
    '^': '<',
    'v': '>',
    '>': 'v',
    '<': '^',
}


class Car:
    def __init__(self, startx, starty, startdir):
        self.xy = startx, starty
        # direction the car is facing: < ^ v >
        self.dir = startdir
        # rotates through LEFT, FORWARD, RIGHT, then back to LEFT
        self.turn_idx = 0

    def __repr__(self):
        return "<Car [{}] at ({},{}) turning {}>".format(
            self.dir, self.xy[0], self.xy[1], TURNS[self.turn_idx])


def get_and_replace_cars(map):
    cars = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            char = map[y][x]
            if char in DIR_VEC_MAP.keys():
                car = Car(x, y, char)
                cars.append(car)
                map[y][x] = REPLACE_CAR_MAP[char]
    return cars, map


def turn(dir, rot):
    """
    dir: Direction currently facing: north/s/e/w
    rot: Rotation of the turn: left, right, straight
    Returns new direction
    """
    # left = -1, straight = 0, right = +1
    step = TURNS.index(rot) - 1
    dir_idx = CLOCKWISE_DIRS.index(dir)
    new_idx = (dir_idx + step) % len(CLOCKWISE_DIRS)
    return CLOCKWISE_DIRS[new_idx]


assert turn('>', LEFT) == '^'
assert turn('<', RIGHT) == '^'


def tick(cars, map):
    """Advance all cars, check for crashes. Returns:
    (x, y, None) if there is a crash at (x,y)
    (None, None, updated cars) if there isn't
    """
    cars = sorted(cars, key=lambda c: c.xy)
    for car in cars:
        x, y = car.xy
        xv, yv = DIR_VEC_MAP[car.dir]
        nextx, nexty = x + xv, y + yv
        # TODO check for collision here
        car_xys = {c.xy for c in cars if c is not car}
        if (nextx, nexty) in car_xys:
            return nextx, nexty
        tile = map[nexty][nextx]
        if tile == '/':
            car.dir = FWD_SLASH_MAP[car.dir]
        if tile == '\\':
            car.dir = BACK_SLASH_MAP[car.dir]
        if tile == '+':
            new_dir = turn(car.dir, TURNS[car.turn_idx])
            car.dir = new_dir
            car.turn_idx = (car.turn_idx + 1) % 3
        car.xy = (nextx, nexty)
    return None, None


def print_map_with_cars(cars, map):
    to_print = []
    car_dict = {(c.xy): c.dir for c in cars}
    for y in range(len(map)):
        for x in range(len(map[0])):
            if (x, y) in car_dict:
                to_print.append(car_dict[(x, y)])
            else:
                to_print.append(map[y][x])
        to_print.append('\n')
    print(''.join(to_print))


with open('in.txt', 'r') as f:
    map = [list(l.replace('\n', '')) for l in f.readlines()]
    cars, map = get_and_replace_cars(map)
    x, y = None, None
    while not x:
        x, y = tick(cars, map)
    # Part 1
    print(x, y)
