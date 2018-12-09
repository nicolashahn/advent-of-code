# input:
# 452 players; last marble is worth 70784 points
# example input:
# 9 players; last marble is worth 32 points (high score 32)

from collections import Counter


players, last_marble = 452, 70784*100
# Part 1
# scores = Counter()
# marbles = [0]
# next_marble = 1
# last_pos = 0
# curr_player = 0
# players, last_marble = 452, 70784
# while next_marble <= last_marble:
#     if next_marble % 23 == 0:
#         score = next_marble
#         last_pos -= 7
#         if last_pos < 0:
#             last_pos = len(marbles) + last_pos
#         removed_marble = marbles.pop(last_pos)
#         score += removed_marble
#         scores[curr_player] += score
#     else:
#         if last_pos >= len(marbles) - 1:
#             last_pos = -1
#         last_pos += 2
#         marbles.insert(last_pos, next_marble)
#     curr_player += 1
#     if curr_player == players:
#         curr_player = 0
#     next_marble += 1
# print(max(scores.values()))


class Node:

    def __init__(self, val):
        self.prev = None
        self.next = None
        self.val = val

    def __str__(self):
        return "<Node {}>".format(self.val)


def print_list(node):
    """ For debuggery. """
    out = []
    start = node
    out += [str(node.val)]
    node = node.next
    while start != node:
        out += [str(node.val)]
        node = node.next
    print('[', ', '.join(out), ']')


# Create circular list
curr = Node(0)
new = Node(1)
curr.next = curr.prev = new
new.next = new.prev = curr
zero = curr
curr = new

player = 2
marble = 2
scores = Counter()

while marble <= last_marble:
    if marble % 23 == 0:
        score = marble
        for _ in range(7):
            curr = curr.prev
        removed = curr
        score += removed.val
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        curr = curr.next
        scores[player] += score
    else:
        last = curr
        curr = curr.next
        node = Node(marble)
        node.next = curr.next
        node.prev = curr
        curr.next = node
        curr.prev = last
        curr = node
    marble += 1
    player += 1
    if player == players:
        player = 0
print(max(scores.values()))
