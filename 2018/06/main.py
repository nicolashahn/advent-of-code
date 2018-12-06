with open('in.txt', 'r') as f:
    coords = [(int(x), int(y)) for x, y in
              [l.split(',') for l in f.readlines()]]
    width = max(coords, key=lambda c: c[0])
    height = max(coords, key=lambda c: c[1])
