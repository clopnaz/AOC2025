#!/usr/bin/env python3
import itertools

directions = []
directions.append([-1,0])
directions.append([+1,0])
directions.append([-1,-1])
directions.append([0,-1])
directions.append([+1,-1])
directions.append([-1,+1])
directions.append([0,+1])
directions.append([+1,+1])

# txt = open('test.txt').read()
txt = open('input.txt').read()
lines = txt.splitlines()
chars = [list(line) for line in lines]
y_max = len(chars)-1
x_max = len(chars[0])-1

def valid_location(y,x):
    if 0<=y<=y_max and 0<=x<=x_max:
        return True
    else:
        return False

def num_surrounding(y,x):
    num = 0
    for direction in directions:
        check_y, check_x = (y + direction[0], x + direction[1])
        if valid_location(check_y, check_x):
            if chars[check_y][check_x] == '@':
                num += 1
    return num


part_1 = 0
matches = []
for y in range(len(chars)):
    for x in range(len(chars[0])):
        if chars[y][x] == '@' and num_surrounding(y, x) < 4:
            matches.append([y,x])
            part_1 += 1
part_2 = 0
found = True
while found:
    found = False
    for y in range(len(chars)):
        # print(f"{y = }")
        for x in range(len(chars[0])):
            # print(f"{x = }")
            if chars[y][x] == '@' and num_surrounding(y, x) < 4:
                matches.append([y,x])
                part_2 += 1
                chars[y][x] = '.'
                found = True
                # for line in chars:
                #     print(''.join(line))
    if not found:
        break
# for y, x in matches:
#     chars[y][x] = 'x'
print(f"{part_1 = }")
print(f"{part_2 = }")

