puzz_in = 320851
# puzz_in = 51589 # part 1 answer: 5158916779, part 2 answer: 9
# puzz_in = 01245
# puzz_in = 92510
# puzz_in = 59414 # p1 2018


recs = [3, 7]

# indices of where the elves currently are in the rec list
elf1 = 0
elf2 = 1


def add_new_recipes(recs, elf1, elf2):
    new_recs = [int(r) for r in str(recs[elf1] + recs[elf2])]
    for rec in new_recs:
        recs.append(rec)
    return recs


def move_elf(elf, recs):
    curr_rec = recs[elf]
    new_pos = (elf + curr_rec + 1) % len(recs)
    return new_pos


while True:
    # recs = add_new_recipes(recs, elf1, elf2)
    new_recs = [int(r) for r in str(recs[elf1] + recs[elf2])]
    for rec in new_recs:
        recs.append(rec)
    elf1 = move_elf(elf1, recs)
    elf2 = move_elf(elf2, recs)
    # print(elf1, elf2)
    if len(recs) == puzz_in + 10:
        break

# Part 1
print(''.join([str(n) for n in recs[-10:]]))



recs = [3, 7]

# indices of where the elves currently are in the rec list
elf1 = 0
elf2 = 1

puzz_in_list = [int(n) for n in str(puzz_in)]
while True:
    new_recs = [int(r) for r in str(recs[elf1] + recs[elf2])]
    for rec in new_recs:
        recs.append(rec)
        last = recs[-len(puzz_in_list):]
        if puzz_in_list == recs[-len(puzz_in_list):]:
            # Part 2
            print(len(recs) - len(puzz_in_list))
            exit()
    elf1 = move_elf(elf1, recs)
    elf2 = move_elf(elf2, recs)
