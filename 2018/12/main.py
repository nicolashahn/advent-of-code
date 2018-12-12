def step(state, offset, rules):
    new_state = ['.', '.']
    for i in range(2, len(state) - 2):
        five = ''.join(state[i - 2:i + 3])
        plant = '#' if five in rules else '.'
        new_state.append(plant)
    new_state += ['.', '.']
    return new_state


def score(state, offset):
    ret = 0
    for i, p in enumerate(state):
        if p == '#':
            ret += i - offset
    return ret


with open('in.txt', 'r') as f:
    lines = f.readlines()
    # number of negative indices
    offset = 200
    state = (['.'] * offset +
             list(lines[0].split(': ')[1].strip()) +
             ['.'] * offset)
    rules = set([line.split()[0] for line in lines[2:]
                 if line.split()[2] == '#'])
    for gen in range(20):
        state = step(state, offset, rules)
    # Part 1
    print(score(state, offset))


with open('in.txt', 'r') as f:
    lines = f.readlines()
    # number of negative indices
    offset = 2000
    state = (['.'] * offset +
             list(lines[0].split(': ')[1].strip()) +
             ['.'] * offset)
    rules = set([line.split()[0] for line in lines[2:]
                 if line.split()[2] == '#'])
    last_score = score(state, offset)
    for gen in range(1000):
        state = step(state, offset, rules)
        new_score = score(state, offset)
        print(gen, new_score, last_score, new_score - last_score)
        last_score = new_score

    print(score(state, offset))


# Part 2 - some manual legwork
# Run the thing until it finds a stable (linearly increasing) state
# Extrapolate from that state's score, multiply the increase by 50,000,000
# minus how many generations it took to get there and add it to the score
'''
>>> score = 32401  # at generation 1000
>>> fiddy = 50000000000
>>> fiddy - 1000
49999999000
>>> (fiddy - 1000) * 32
1599999968000
>>> (fiddy - 1000) * 32 + score
1600000000401  # <- this was my answer
'''
