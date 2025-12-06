#!/usr/bin/env python3
import itertools

# txt = open('test.txt').read()
txt = open('input.txt').read()
part_1 = 0
def joltage(batts, nleft):
    if nleft:
        batt = max(batts[:-nleft])
    else:
        batt = max(batts)
    remaining = batts[batts.index(batt)+1:]
    return batt, remaining


part_1 = 0
part_2 = 0
for line in txt.splitlines():
    batts = [int(c) for c in list(line)]
    batts2 = batts.copy()
    # batt_1 = max(batts[:-1])
    jolted1 = []
    for num_batts_left in reversed(range(2)):
        jolted1, batts = joltage(batts, num_batts_left)
        part_1 += jolted1 * 10**num_batts_left

    for num_batts_left in reversed(range(12)):
        jolted1, batts2 = joltage(batts2, num_batts_left)
        part_2 += jolted1 * 10**num_batts_left

print(f"{part_1}") 
print(f"{part_2}") 
