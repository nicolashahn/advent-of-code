with open('in.txt', 'r') as f:
    lines = f.readlines()
    claims = []
    for line in lines:
        id, _, raw_coords, raw_dims = line.split()
        coords = tuple(int(n) for n in raw_coords[:-1].split(','))
        dims = tuple(int(n) for n in raw_dims.split('x'))
        claims.append((id, coords, dims))
    grid = []
    for _ in range(1000):
        grid.append([0 for _ in range(1000)])
    for _, coords, dims in claims:
        x, y = coords
        w, h = dims
        for i in range(y, y + h):
            for j in range(x, x + w):
                grid[i][j] += 1
    ct = 0
    for i in range(1000):
        for j in range(1000):
            ct += 1 if grid[i][j] > 1 else 0
    # Part 1
    print(ct)

    for id, coords, dims in claims:
        x, y = coords
        w, h = dims
        overlap = False
        for i in range(y, y + h):
            for j in range(x, x + w):
                if grid[i][j] != 1:
                    overlap = True
                    break
        if not overlap:
            # Part 2
            print(id)
            break
