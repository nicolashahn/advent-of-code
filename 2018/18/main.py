from collections import defaultdict

def get_adjs(x, y, grid):
    adjs = []
    for ax, ay in (
        (x + 1, y),
        (x - 1, y),
        (x + 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x, y + 1),
        (x, y - 1),
    ):
        if (0 <= ax < len(grid[0])) and (0 <= ay < len(grid)):
            adjs.append(grid[ay][ax])
    return adjs


def step_cell(x, y, grid):
    adjs = get_adjs(x, y, grid)
    cell = grid[y][x]
    if cell == '.':
        if len([a for a in adjs if a == '|']) >= 3:
            return '|'
        else:
            return '.'
    elif cell == '|':
        if len([a for a in adjs if a == '#']) >= 3:
            return '#'
        else:
            return '|'
    elif cell == '#':
        if '|' in adjs and '#' in adjs:
            return '#'
        else:
            return '.'


def step_grid(grid):
    next_grid = [[None for _ in range(len(grid[0]))]
                 for _ in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            next_grid[y][x] = step_cell(x, y, grid)
    return next_grid


def get_score(grid):
    wooded = lumberyards = 0
    for row in grid:
        for cell in row:
            if cell == '|':
                wooded += 1
            elif cell == '#':
                lumberyards += 1
    return wooded * lumberyards


def p1(lines):
    last = 0
    grid = [line.strip() for line in lines]
    for _ in range(10):
        grid = step_grid(grid)
        # print('\n'.join([''.join(row) for row in grid]))
        score = get_score(grid)
        last = score
    print(last)


def p2(lines):
    last = 0
    grid = [line.strip() for line in lines]
    ctr = defaultdict(list)
    for i in range(1, 1001):
        grid = step_grid(grid)
        # print('\n'.join([''.join(row) for row in grid]))
        score = get_score(grid)
        ctr[score].append(i)
        last = score
    for k, v in ctr.items():
        print(k, v)
    print(last)

# Part 2:
# Part 2:

# Use the ctr above to produce the score: minute mapping, which starts
# repeating at 564:
"""
189150 [564, 566, 594, 622, 650, 678, 706, 734, 762, 790, 818, 846, 874, 902, 930, 958, 986]
187404 [565, 593, 621, 649, 677, 705, 733, 761, 789, 817, 845, 873, 901, 929, 957, 985]
190125 [567, 595, 623, 651, 679, 707, 735, 763, 791, 819, 847, 875, 903, 931, 959, 987]
192603 [568, 596, 624, 652, 680, 708, 736, 764, 792, 820, 848, 876, 904, 932, 960, 988]
192831 [569, 597, 625, 653, 681, 709, 737, 765, 793, 821, 849, 877, 905, 933, 961, 989]
196578 [570, 598, 626, 654, 682, 710, 738, 766, 794, 822, 850, 878, 906, 934, 962, 990]
199424 [571, 599, 627, 655, 683, 711, 739, 767, 795, 823, 851, 879, 907, 935, 963, 991]
202572 [572, 600, 628, 656, 684, 712, 740, 768, 796, 824, 852, 880, 908, 936, 964, 992]
205461 [573, 601, 629, 657, 685, 713, 741, 769, 797, 825, 853, 881, 909, 937, 965, 993]
208884 [574, 602, 630, 658, 686, 714, 742, 770, 798, 826, 854, 882, 910, 938, 966, 994]
214520 [576, 604, 632, 660, 688, 716, 744, 772, 800, 828, 856, 884, 912, 940, 968, 996]
218673 [577, 605, 633, 661, 689, 717, 745, 773, 801, 829, 857, 885, 913, 941, 969, 997]
219566 [578, 606, 634, 662, 690, 718, 746, 774, 802, 830, 858, 886, 914, 942, 970, 998]
219919 [579, 607, 635, 663, 691, 719, 747, 775, 803, 831, 859, 887, 915, 943, 971, 999]
221340 [580, 608, 636, 664, 692, 720, 748, 776, 804, 832, 860, 888, 916, 944, 972]
219745 [581, 609, 637, 665, 693, 721, 749, 777, 805, 833, 861, 889, 917, 945, 973]
218584 [582, 610, 638, 666, 694, 722, 750, 778, 806, 834, 862, 890, 918, 946, 974]
219096 [583, 611, 639, 667, 695, 723, 751, 779, 807, 835, 863, 891, 919, 947, 975]
216948 [584, 612, 640, 668, 696, 724, 752, 780, 808, 836, 864, 892, 920, 948, 976]
210888 [585, 613, 641, 669, 697, 725, 753, 781, 809, 837, 865, 893, 921, 949, 977]
206568 [586, 614, 642, 670, 698, 726, 754, 782, 810, 838, 866, 894, 922, 950, 978]
204417 [587, 615, 643, 671, 699, 727, 755, 783, 811, 839, 867, 895, 923, 951, 979]
202980 [588, 616, 644, 672, 700, 728, 756, 784, 812, 840, 868, 896, 924, 952, 980]
198990 [589, 617, 645, 673, 701, 729, 757, 785, 813, 841, 869, 897, 925, 953, 981]
197819 [590, 618, 646, 674, 702, 730, 758, 786, 814, 842, 870, 898, 926, 954, 982]
191478 [592, 620, 648, 676, 704, 732, 760, 788, 816, 844, 872, 900, 928, 956, 984]
"""
# We find that the repetition period = 28
# Then, pick one of these (say 650) and subtract it from $NUM_MINS (1000000000)
# and apply modulo: (1000000000 - 650) % 28 = 14
# Find the score of the minute that is 14 - 1 past 650: 219919


with open('in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
