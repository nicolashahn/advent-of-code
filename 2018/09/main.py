# input:
# 452 players; last marble is worth 70784 points
# example input:
# 9 players; last marble is worth 32 points (high score 32)

from collections import Counter

scores = Counter()

marbles = [0]
next_marble = 1
last_pos = 0
curr_player = 0

players, last_marble = 452, 70784*100
# players, last_marble = 452, 70784
while next_marble <= last_marble:
    if next_marble % 23 == 0:
        score = next_marble
        last_pos -= 7
        if last_pos < 0:
            last_pos = len(marbles) + last_pos
        removed_marble = marbles.pop(last_pos)
        print(next_marble, removed_marble, curr_player)
        score += removed_marble
        scores[curr_player] += score
    else:
        if last_pos >= len(marbles) - 1:
            last_pos = -1
        last_pos += 2
        marbles.insert(last_pos, next_marble)
    curr_player += 1
    if curr_player == players:
        curr_player = 0
    next_marble += 1
# Part 1, 2
print(max(scores.values()))
