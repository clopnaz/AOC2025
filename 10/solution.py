#!/usr/bin/env python3

from __future__ import annotations

import collections
import dataclasses
import functools
import itertools
from multiprocessing import Pool
import re
# import matplotlib
# from matplotlib import pyplot

directions = []
directions.append([-1,0])
directions.append([+1,0])
directions.append([-1,-1])
directions.append([0,-1])
directions.append([+1,-1])
directions.append([-1,+1])
directions.append([0,+1])
directions.append([+1,+1])

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


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise(IndexError(key))

    @functools.cached_property
    def list(self):
        return [self.x, self.y]

    def is_on(self, other: Segment):
        return other.contains(self) or self in (other.a, other.b)

@dataclasses.dataclass
class Segment:
    a: Point
    b: Point

    def __post_init__(self):
        try:
            assert any(self.direction) and not all(self.direction)
        except:
            breakpoint()
            pass

    @functools.cached_property
    def list(self):
        return [self.a.list, self.b.list]

    @functools.cached_property
    def direction(self):
        direction = [self.b[0]-self.a[0], self.b[1]-self.a[1]]
        for n in range(len(direction)):
            if direction[n]:
                direction[n] = direction[n] // abs(direction[n])
        return tuple(direction)

    @functools.cached_property
    def norm(self):
        return (-self.direction[1], self.direction[0])

    def contains(self, other: Point):
        if self.direction[0]:
            var_idx = 0
            const_idx = 1
        else:
            var_idx = 1
            const_idx = 0
        return (
                (
                    self.a[var_idx] < other[var_idx] < self.b[var_idx] or
                    self.a[var_idx] > other[var_idx] > self.b[var_idx]
                ) and (
                    self.a[const_idx] == other[const_idx]
                ))

    def intersects(self, other: Point):
        # . . . . . . . . . . .
        # . . . . . . . . . . .
        # . . . | . . . . . . .
        # . - - - - - . . . . .
        # . . . | . . . . . . .
        # . . . | . . . . . . .
        # . . . . . . . . . . .
        # . . . . . . . . . . .
        # a = 1,4
        # b = 5,4
        # a = 3,2
        # b = 3,5

        if self.direction == other.direction:
            return False
        if self.direction[0]:
            possible_cross = Point(other.a[0], self.a[1])
        else:
            possible_cross = Point(self.a[0], other.a[1])
        return (self.contains(possible_cross) and other.contains(possible_cross))

    @property
    def line_collection(self):
        return matplotlib.collections.LineCollection([[self.a.list, self.b.list]])


@dataclasses.dataclass
class Polygon:
    segments: list(Segment)

    @functools.cached_property
    def points(self):
        points = set()
        for segment in self.segments:
            for point in segment.list:
                points.update([Point(point[0], point[1])])
        return points

    @functools.cached_property
    def point_combinations(self):
        return tuple(itertools.combinations(self.points, 2))

    def __iter__(self):
        return iter(self.segments)

    def covers(self, other: Rectangle):
        for point in self.points:
            if other.contains(point):
                return False
        for rect_segment in other.segments:
            for poly_segment in self.segments:
                if rect_segment.intersects(poly_segment):
                    # ax = pyplot.gca()
                    # c0 = other.line_collection
                    # c0.set_color('black')
                    # c0.set_linewidth(0.5)
                    # ax.add_collection(c0)
                    # c1 = poly_segment.line_collection
                    # c1.set_color('green')
                    # c1.set_linewidth(5)
                    # ax.add_collection(c1)
                    # c2 = rect_segment.line_collection
                    # c2.set_color('red')
                    # c2.set_linewidth(1)
                    # ax.add_collection(c2)
                    # ax.plot([other.p1.list, other.p2.list], color='magenta', marker='o')
                    # breakpoint()
                    return False
        return True



@dataclasses.dataclass
class Rectangle:
    p1: Point
    p2: Point

    @functools.cached_property
    def area(self):
        return get_area(self.p1, self.p2)

    def __lt__(self, other):
        return self.area < other.area

    def __gt__(self, other):
        return self.area > other.area

    def __eq__(self, other):
        return self.area == other.area

    def contains(self, other: Point):
        return (
                    self.p1[0] < other[0] < self.p2[0]
                    or self.p1[0] > other[0] > self.p2[0]
                ) and (
                    self.p1[1] < other[1] < self.p2[1]
                    or self.p1[1] > other[1] > self.p2[1]
                )

    @functools.cached_property
    def pa(self):
        return Point(self.p1[0], self.p2[1])

    @functools.cached_property
    def pb(self):
        return Point(self.p2[0], self.p1[1])

    @property
    def segments(self):
        return [
                Segment(self.p1, self.pa),
                Segment(self.pa, self.p2),
                Segment(self.p2, self.pb),
                Segment(self.pb, self.p1),
                ]
    @property
    def line_collection(self):
        l = [s.list for s in self.segments]
        return matplotlib.collections.LineCollection(l, linewidths=2)

def parse(line):
    # return re.match(r'\[([^\]]+)\] ((\(?:[^)]+\) )+\{[^\}]+\}', line).groups()
    match = re.match(r'\[([^\]]+)\] ((:?\([^)]+\) )+)\{([^}]+)\}', line)
    lights, buttons, _, jolts = match.groups()
    lights = tuple(lights)
    buttons = tuple(s.split(',') for s in tuple(s for s in buttons.strip(' ()').replace(') (', ' ').split()))
    return make_lights(lights, buttons, jolts)

@dataclasses.dataclass(frozen=True)
class Joltage():
    tuple: list[int]
    def __post_init__(self):
        if getattr(self.tuple, '__hash__') is None:
            raise ValueError(f"Unhashable Type tuple: {type(self.tuple)}")
    def __add__(self, other):
        return Joltage(tuple(map(lambda x,y: x+y, self.tuple, other.tuple)))
    def __eq__(self, other):
        return list(self.tuple) == list(other.tuple)
    def __index__(self, b):
        return self.tuple.__index__(b)
    def __getitem__(self, b):
        return self.tuple.__getitem__(b)
    def press(self, button, times=1):
        new = list(self.tuple)
        for idx in button:
            new[idx] += times
        return Joltage(tuple(new))

test_j1 = Joltage((1,2,3))
test_j2 = Joltage((0,1,2))
assert test_j1 + test_j2 == Joltage((1,3,5))
assert test_j1.press((0,2)) == Joltage((2,2,4))

@dataclasses.dataclass(frozen=True)
class Lights():
    target_values: tuple[bool]
    buttons: tuple[tuple[int]]
    target_joltage: tuple[int]


    def press(self, which):
        # print('press')
        lit = [False for _ in range(len(self.target_values))]
        for button_num in which:
            button = self.buttons[button_num]
            # print(f"{button = }")
            for idx in button:
                lit[idx] = lit[idx] ^ True
        return tuple(lit)

    def check(self, which):
        # print('check')
        lit = self.press(which)
        return self.target_values == lit

    def search(self, num_presses):
        # print(num_presses)
        self.eliminate_buttons()
        for which in itertools.combinations(range(len(self)), num_presses):
            if self.check(which):
                return True
        return False

    # @functools.lru_cache(maxsize=None)
    def press_once2(self, button_num, times=1):
        # print("press_once2: {button_num}")
        joltage = [0]*len(self.target_joltage)
        for idx in self.buttons[button_num]:
            joltage[idx] += 1
        return joltage

    # @functools.lru_cache(maxsize=None)
    def press2(self, which):
        joltage = [0]*len(self.target_joltage)
        for which_button, num_presses in collections.Counter(which).items():
            map(lambda x,y: x+y, joltage, self.press_once2(which_button, num_presses))
        return tuple(joltage)

        # # print(f"press2: {which}")
        # if len(which) == 1:
        #     return self.press_once2(which[0])
        # return map(lambda x,y: x+y, self.press_once2(which[0]), self.press2(which[1:]))

    def check2(self, which):
        # print(f"check2")
        joltage = self.press2(which)
        return self.target_joltage == joltage

    def search2(self, num_presses):
        for which in itertools.combinations_with_replacement(range(len(self)), num_presses):
            sorted(which)
            # print(which)
            # if self.check2(which):
            #     return True
        return False

    def __len__(self):
        return len(self.buttons)

    def eliminate_buttons(self):
        current_presses = collections.Counter()
        current_joltage = [0]*len(self.target_joltage)
        for idx, joltage in enumerate(self.target_joltage):
            idx_buttons = self.buttons



def make_lights(target_values, buttons, target_joltage):
        target_values = tuple([s == '#' for s in target_values])
        buttons = tuple([tuple(map(int, s)) for s in buttons])
        target_joltage = tuple(map(int, target_joltage.split(',')))
        return Lights(target_values, buttons, target_joltage)


if __name__ == '__main__':
    # txt = open('test.txt').read()
    txt = open('input.txt').read()
    lines = txt.splitlines()
    part_1 = 0
    for line in lines:
        lights = parse(line)
        num_presses = 0
        while True:
            if lights.search(num_presses):
                # print(f"{num_presses = }")
                part_1 += num_presses
                break
            num_presses += 1
    assert part_1 in [7, 385]
    for line in lines:
        lights = parse(line)
        # print(lights)
        num_presses = 10
        while True:
            if lights.search2(num_presses):
                print(f"{num_presses = }")
                break
            print(f"{num_presses = }")
            num_presses += 1

