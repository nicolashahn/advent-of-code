from collections import Counter

def dist(x1y1, x2y2):
    x1, y1 = x1y1
    x2, y2 = x2y2
    return abs(x1 - x2) + abs(y1 - y2)


with open('in.txt', 'r') as f:
    # create coordinate: value map
    coords = [(int(x), int(y)) for x, y in
              [l.split(',') for l in f.readlines()]]
    cmap = {xy: i + 1 for i, xy in enumerate(coords)}

    # generate 2d matrix
    width = max(coords, key=lambda c: c[0])[0]
    height = max(coords, key=lambda c: c[1])[1]
    matrix = [[0 for x in range(width + 2)]
              for y in range(height + 2)]

    # get closest distances for each empty point
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            dists = {}
            for x2y2 in cmap.keys():
                dists[x2y2] = dist((x, y), x2y2)
            best_xy = min(dists, key=dists.get)
            if len([xy for xy in dists if dists[xy] == dists[best_xy]]) > 1:
                matrix[y][x] = -1
            else:
                matrix[y][x] = cmap[best_xy]

    # values on the edges of the matrix are infinite
    infinite = set(
        matrix[0] +
        matrix[-1] +
        [r[0] for r in matrix] +
        [r[-1] for r in matrix]
    )

    # flatten the matrix
    matrix_1d = []
    for row in matrix:
        matrix_1d += row

    # filter infinite values
    matrix_1d = [x for x in matrix_1d if x not in infinite and x != -1]
    ctr = Counter(matrix_1d)

    # Part 1
    print(max(ctr.values()))
