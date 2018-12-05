from datetime import datetime
import re


with open('in.txt', 'r') as f:
    lines = sorted(f.readlines())
    guards = {}
    guard = None
    last_min = None
    for line in lines:
        minute = int(re.search('\:(\d\d)\]', line).group(1))
        guard_re = re.search('#(\d+)', line)
        if guard_re:
            guard = int(guard_re.group(1))
            last_min = None
        elif 'falls' in line:
            last_min = minute
        elif 'wakes' in line:
            if guard not in guards:
                guards[guard] = [0 for _ in range(60)]
            for i in range(last_min, minute):
                guards[guard][i] += 1
            last_min = None
    sleepiest = max(guards, key=lambda g: sum(guards[g]))
    sleepy_min = guards[sleepiest].index(max(guards[sleepiest]))
    # Part 1
    print(sleepiest * sleepy_min)
    
    max_min = -1
    ans = None
    for guard, mins in guards.items():
        if max(mins) > max_min:
            max_min = max(mins)
            ans = guard * mins.index(max_min)
    # Part 2
    print(ans)
