from collections import Counter


# Part 1
with open('in.txt', 'r') as f:
    boxes = f.readlines()
    twos = threes = 0
    for box in boxes:
        bctr = Counter(box)
        hastwo = [k for k, v in bctr.items() if v == 2]
        hasthree = [k for k, v in bctr.items() if v == 3]
        if hastwo:
            twos += 1
        if hasthree:
            threes += 1
    print(twos * threes)

# Part 2
with open('in.txt', 'r') as f:
    boxes = [b.strip() for b in f.readlines()]
    for i, box1 in enumerate(boxes[:-1]):
        for box2 in boxes[i + 1:]:
            common = []
            for j, c in enumerate(box1):
                if box2[j] == c:
                    common.append(c)
            if len(common) == len(box1) - 1:
                print(''.join(common))
                break
