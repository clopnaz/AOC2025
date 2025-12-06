#!/usr/bin/env python3
import itertools

txt = open('test.txt').read()
# txt = open('input.txt').read()
ranges = txt.split(',')


def has_repeat(i):
    i = str(i)
    len_i = len(i)
    if not(len_i % 2) and i[:len_i//2] == i[len_i//2:]:
        return True
    return False

def has_repeat_2(i):
    i = str(i)
    len_i = len(i)
    for sub_len in range(1,len_i//2+1):
        if len(set(itertools.batched(i, sub_len))) == 1:
            return True
    return False

part_1 = 0
part_2 = 0
for r in ranges:
    print(r)
    (first_id, last_id) = map(int, r.split('-'))
    for ID in range(first_id, last_id+1):
        if has_repeat(ID):
            part_1 += ID
        if has_repeat_2(ID):
            part_2 += ID






print(f"{part_1 = }")
print(f"{part_2 = }")
