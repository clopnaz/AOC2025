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

# txt = open('test.txt').read()
txt = open('input.txt').read()

lines = txt.splitlines()
lines = [[x for x in line.strip().split(' ') if x] for line in lines]
part_1 = 0
while any(lines):
    # print(lines)
    math = []
    for line in lines:
        math.append(line.pop(0))
    op = math.pop(-1)
    math = [int(c) for c in math]
    if op == '*':
        def func(x,y):
            return x * y
    elif op == '+':
        def func(x,y):
            return x + y
    else:
        print(f"bad operation {op = }")
        exit()
    partial = functools.reduce(func, math)
    part_1 += partial
    # print(f"{partial = }")
print(f"{part_1 = }")

lines = [list(line) for line in txt.splitlines()]
part_2 = 0
print(txt)
print(lines)
nums = []
while all(lines):
    # read nothing, or
    # read a number, optionally an operation. if an operation, calculate
    line = [x for x in [line.pop() for line in lines] if x]
    op = line.pop().strip()
    num_str = ''.join(line).strip()
    if num_str:
        nums.append(int(num_str))
    if op:
        if op == '*':
            def func(x,y):
                return x * y
        elif op == '+':
            def func(x,y):
                return x + y
        else:
            print(f"bad operation {op = }")
            exit()
        partial = functools.reduce(func, nums)
        print(f"{partial = }")
        part_2 += partial
        nums = []
print(f"{part_2 = }")
