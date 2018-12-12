def step(state, offset, rules):
    # if '#' in state[:4]:
        # state = ['.'] * 4 + state
        # offset += 4
        # new_state = ['.'] * 4
    # if '#' in state[-2:]:
        # state += ['.'] * 4
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
    offset = 200
    state = (['.'] * offset +
             list(lines[0].split(': ')[1].strip()) +
             ['.'] * offset)
    # number of negative indices
    rules = set([line.split()[0] for line in lines[2:]
                 if line.split()[2] == '#'])
    print(rules)
    for _ in range(20):
        # print(''.join(state))
        state = step(state, offset, rules)
    # print(''.join(state))

    # Part 1
    print(score(state, offset))
