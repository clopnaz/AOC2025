#!/usr/bin/env python3
import itertools
import functools
from multiprocessing import Pool

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
# squares = [(x,y) for (x,y) in line.strip().split() for line in lines]

def distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**.5

def get_area(a,b):
    return (1 + abs(b[1] - a[1]))*(1 + abs(b[0] - a[0]))

#  . a . d . 1
#  . . . . . 2
#  . c . b . 3
#  1 2 3 4 5
# a = 1 2
# b = 3 4
# c = 3 2 = (b[0] a[1])
# d = 1 4 = (a[0] b[1])

@functools.cache
def make_walls(a,b):
    c = (a[0], b[1])
    d = (b[0], a[1])
    walls = set()
    walls.update(make_line(a,c))
    walls.update(make_line(c,b))
    walls.update(make_line(b,d))
    walls.update(make_line(d,a))
    return walls

def make_line(a, b):
    if a[0] == b[0]:
        if a[1] < b[1]:
            y1, y2 = a[1], b[1]
        else:
            y1, y2 = b[1], a[1]
        return [(a[0], y) for y in range(y1,y2)]
    elif a[1] == b[1]:
        if a[0] < b[0]:
            y1, y2 = a[0], b[0]
        else:
            y1, y2 = b[0], a[0]
        return [(y, a[1]) for y in range(y1,y2)]
    else:
        raise ValueError(f"{a = }, {b = }")

def toward(a,b):
    dx = (b[0] - a[0])
    dy = (b[1] - a[1])
    if dx == 0:
        x = 0
    else:
        x = dx // abs(dx)
    if dy == 0:
        y = 0
    else:
        y = dy // abs(dy)
    return (x,y)

def is_inside(a):
    if a in borders:
        return True
    (x,y) = a
    crosses = 0
    while x > x_floor and y > y_floor:
        if (x,y) in borders:
            crosses += 1
        x -= 1
        y -= 1
    return bool(crosses % 2)

def in_rect(a, rect):
    recta, rectb = rect
    if recta[0] < a[0] < rectb[0] or rectb[0] < a[0] < recta[0]:
        if recta[1] < a[1] < rectb[1] or rectb[1] < a[1] < recta[1]:
            return True
    return False

def any_in_rect(rect):
    for red in reds:
        if in_rect(red, rect):
            return True
    return False

def segment_crosses_rect(segment, rect):
    sega, segb = segment
    recta, rectb = rect
    if sega[0] == segb[0]:
        if recta[0] < sega[0] < rectb[0] or rectb[0] < sega[0] < recta[0]:
            if (sega[1] < recta[1] < segb[1] or segb[1] < recta[1] < sega[1]
                or sega[1] < rectb[1] < segb[1] or segb[1] < rectb[1] < sega[1]):
                return True
    elif sega[1] == segb[1]:
        if recta[1] < sega[1] < rectb[1] or rectb[1] < sega[1] < recta[1]:
            if (sega[0] < recta[0] < segb[0] or segb[0] < recta[0] < sega[0]
                or sega[0] < rectb[0] < segb[0] or segb[0] < rectb[0] < sega[0]):
                return True
    else:
        raise ValueError(f"{segment = }, {rect = }")
    return False

def any_segment_crosses_rect(rect):
    for segment in segments:
        if segment_crosses_rect(segment, rect):
            return True
    return False

def check_corners(rect):
    a,b = rect
    c = (a[0], b[1])
    d = (b[0], a[1])
    return is_inside(a) and is_inside(b)

reds = []
x_vals = []
y_vals = []
for line in lines:
    x,y = map(int,line.strip().split(','))
    x_vals.append(x)
    y_vals.append(y)
    square = (int(x),int(y))
    reds.append(square)
x_floor = min(x_vals) - 1
y_floor = min(y_vals) - 1

borders = set()
segments = []
for i in range(len(reds)):
    j = i-1
    segments.append((reds[i], reds[j]))
    new_line = make_line(reds[i], reds[j])
    assert new_line
    borders.update(new_line)

areas = []
areas2 = []
for a, b in itertools.combinations(reds, 2):
    areas.append((get_area(a,b), a, b))
areas.sort(reverse=True)
print(areas[0])
for area in areas:
    (_, a, b) = area
    if not any_segment_crosses_rect((a,b)):
        if not any_in_rect((a,b)):
            if check_corners((a,b)):
                print(area)
                breakpoint()
breakpoint()
# 1428829072
# 1301836184
areas.sort()
areas2.sort()

print(areas[-1])
print(areas2[-1])
breakpoint()
