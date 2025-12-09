#!/usr/bin/env python3
import itertools
import functools

directions = []
directions.append([-1,0])
directions.append([+1,0])
directions.append([-1,-1])
directions.append([0,-1])
directions.append([+1,-1])
directions.append([-1,+1])
directions.append([0,+1])
directions.append([+1,+1])

txt = open('test.txt').read()
txt = open('input.txt').read()
def line_filter(c):
    if c == 'S':
        return '1'
    if c == '.':
        return '0'
    else:
        return c
lines = [list(map(line_filter, list(line))) for line in txt.splitlines()]

part_1 = 0
for y in range(len(lines)):
    if y == 0:
        continue
    for x in range(len(lines[y])):
        if lines[y-1][x].isnumeric() and int(lines[y-1][x])>0:
            if lines[y][x] == '^':
                part_1 += 1
                lines[y][x-1] = str(int(lines[y][x-1]) + int(lines[y-1][x]))
                lines[y][x+1] = str(int(lines[y][x+1]) + int(lines[y-1][x]))
            else:
                lines[y][x] = str(int(lines[y][x]) + int(lines[y-1][x]))

def  un_filter(c):
    if c.isnumeric():
        if int(c) == 0:
            return '.'
        else:
            return '|'
    else:
        return c

print('\n'.join([''.join(map(un_filter, line)) for line in lines]))
# print('\n'.join(['\t'.join(line) for line in lines]))
print(f"{part_1 = }")
part_2 = sum([int(n) for n in lines[-1] if n.isnumeric()])
print(f"{part_2 = }")

